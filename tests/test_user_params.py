"""Проверки группы user_params: multipart-upload, uploadings, uploading, confirm.

Офлайн: respx мокает transport; multipart-тело запроса разбирается по байтам.
"""

from pathlib import Path

import httpx
import pytest
import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.user_params import UserParams
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

runner = CliRunner()
BASE = "https://api-metrika.yandex.net"

CSV = b"UserId,KeyId,ParamValue\n123,42,premium\n"

UPLOADING = {"id": 1, "status": "processed", "action": "update"}


def make_client() -> Client:
    return Client(Config(token="T"))


def write_csv(tmp_path: Path) -> str:
    path = tmp_path / "params.csv"
    path.write_bytes(CSV)
    return str(path)


# -- registry ---------------------------------------------------------------


def test_user_params_endpoints() -> None:
    eps = registry.by_group(registry.ENDPOINTS, registry.GROUPS)["user_params"]
    assert {ep.op for ep in eps} == {"upload", "uploadings", "uploading", "confirm"}
    upload = registry.get_endpoint("user_params", "upload")
    assert upload.method == "POST"
    assert upload.multipart is True


# -- api: multipart upload ---------------------------------------------------


@respx.mock
def test_upload_multipart_body(tmp_path: Path) -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/42/user_params/uploadings/upload"
    ).respond(json={"uploading": UPLOADING})
    with make_client() as c:
        payload = UserParams(c).upload(42, write_csv(tmp_path))
    assert route.called
    assert payload == {"uploading": UPLOADING}

    req = respx.calls[-1].request
    assert "multipart/form-data" in req.headers["content-type"]
    body = req.read()
    # файл уходит form-полем "file" с содержимым CSV, а не JSON-телом
    assert b'name="file"' in body
    assert b'filename="params.csv"' in body
    assert CSV in body
    # action обязателен (openapi), default — update
    assert req.url.params["action"] == "update"


@respx.mock
def test_upload_action_delete_keys(tmp_path: Path) -> None:
    respx.post(f"{BASE}/management/v1/counter/1/user_params/uploadings/upload").respond(
        json={"uploading": {}}
    )
    with make_client() as c:
        UserParams(c).upload(1, write_csv(tmp_path), action="delete_keys")
    assert respx.calls[-1].request.url.params["action"] == "delete_keys"


@respx.mock
def test_upload_retry_429_resends_body(tmp_path: Path, monkeypatch) -> None:
    """Регресс: file handle после первой отправки в EOF — ретрай шлёт
    пустой файл. Тело держится bytes, оба POST несут полный CSV."""
    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: None)
    route = respx.post(
        f"{BASE}/management/v1/counter/1/user_params/uploadings/upload"
    ).mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json={"uploading": {}}),
        ]
    )
    with make_client() as c:
        UserParams(c).upload(1, write_csv(tmp_path))
    assert route.call_count == 2
    for call in route.calls:
        assert CSV in call.request.read()


# -- api: чтение ------------------------------------------------------------


@respx.mock
def test_uploadings_path_and_params() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/7/user_params/uploadings").respond(
        json={"uploadings": []}
    )
    with make_client() as c:
        UserParams(c).uploadings(7, limit=10, offset=5)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["limit"] == "10"
    assert req.url.params["offset"] == "5"


@respx.mock
def test_uploading_path() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/7/user_params/uploading/99"
    ).respond(json={"uploading": {"id": 99}})
    with make_client() as c:
        payload = UserParams(c).uploading(7, 99)
    assert route.called
    assert payload == {"uploading": {"id": 99}}


@respx.mock
def test_confirm_path_without_body() -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/7/user_params/uploading/99/confirm"
    ).respond(json={"uploading": {"id": 99, "status": "is_processed"}})
    with make_client() as c:
        payload = UserParams(c).confirm(7, 99)
    assert route.called
    assert payload == {"uploading": {"id": 99, "status": "is_processed"}}
    # без --data тела нет
    assert respx.calls[-1].request.read() == b""


@respx.mock
def test_confirm_with_body() -> None:
    respx.post(
        f"{BASE}/management/v1/counter/7/user_params/uploading/99/confirm"
    ).respond(json={"uploading": {"id": 99}})
    with make_client() as c:
        UserParams(c).confirm(7, 99, uploading={"id": 99})
    body = respx.calls[-1].request.read()
    assert b'"uploading"' in body
    assert b'"id":99' in body.replace(b" ", b"")


# -- CLI --------------------------------------------------------------------


def test_upload_requires_existing_file(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["user_params", "upload", "42", "--file", str(tmp_path / "nope.csv")]
    )
    assert result.exit_code != 0
    assert "не найден" in result.output


@respx.mock
def test_cli_upload_happy_path(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("METRIKA_TOKEN", "T")
    respx.post(
        f"{BASE}/management/v1/counter/42/user_params/uploadings/upload"
    ).respond(json={"uploading": UPLOADING})
    result = runner.invoke(
        app, ["user_params", "upload", "42", "--file", write_csv(tmp_path)]
    )
    assert result.exit_code == 0
    assert '"status": "processed"' in result.output
