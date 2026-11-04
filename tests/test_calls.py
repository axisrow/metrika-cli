"""Проверки группы calls: multipart-upload, uploadings, uploading.

Офлайн: respx мокает transport; multipart-тело запроса разбирается по байтам.
"""

from pathlib import Path

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.calls import Calls
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

runner = CliRunner()
BASE = "https://api-metrika.yandex.net"

CSV_HEADER = b"ClientId,DateTime,Price,Currency,PhoneNumber"


def make_client() -> Client:
    return Client(Config(token="T"))


def write_csv(tmp_path: Path) -> str:
    path = tmp_path / "calls.csv"
    path.write_bytes(CSV_HEADER + b"\n123,2026-11-05 12:00:00,100,RUB,+79001234567\n")
    return str(path)


# -- registry ----------------------------------------------------------------


def test_calls_endpoints() -> None:
    eps = registry.by_group(registry.ENDPOINTS, registry.GROUPS)["calls"]
    assert [ep.op for ep in eps] == ["upload", "uploading", "uploadings"]
    upload = registry.get_endpoint("calls", "upload")
    assert upload.method == "POST"
    assert upload.multipart is True
    assert "upload_calls" in upload.path


# -- api: multipart ----------------------------------------------------------


@respx.mock
def test_upload_multipart_body(tmp_path: Path) -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/42/offline_conversions/upload_calls"
    ).respond(json={"uploading": {"id": 1, "status": "processed"}})
    with make_client() as c:
        payload = Calls(c).upload(42, write_csv(tmp_path), client_id_type="CLIENT_ID")
    assert route.called
    assert payload == {"uploading": {"id": 1, "status": "processed"}}

    req = respx.calls[-1].request
    assert "multipart/form-data" in req.headers["content-type"]
    body = req.read()
    # файл уходит form-полем "file" с содержимым CSV, а не JSON-телом
    assert b'name="file"' in body
    assert b'filename="calls.csv"' in body
    assert CSV_HEADER in body


@respx.mock
def test_upload_query_params(tmp_path: Path) -> None:
    respx.post(
        f"{BASE}/management/v1/counter/1/offline_conversions/upload_calls"
    ).respond(json={"uploading": {}})
    with make_client() as c:
        Calls(c).upload(
            1,
            write_csv(tmp_path),
            client_id_type="YCLID",
            comment="коллтрекинг",
            new_goal_name="Звонки",
        )
    req = respx.calls[-1].request
    assert req.url.params["client_id_type"] == "YCLID"
    assert req.url.params["comment"] == "коллтрекинг"
    assert req.url.params["new_goal_name"] == "Звонки"


@respx.mock
def test_upload_retry_429_resends_body(tmp_path: Path, monkeypatch) -> None:
    """Регресс: ретрай после 429 шлёт тот же полный CSV (тело держится bytes)."""
    import httpx

    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: None)
    route = respx.post(
        f"{BASE}/management/v1/counter/1/offline_conversions/upload_calls"
    ).mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json={"uploading": {}}),
        ]
    )
    with make_client() as c:
        Calls(c).upload(1, write_csv(tmp_path), client_id_type="CLIENT_ID")
    assert route.call_count == 2
    for call in route.calls:
        assert CSV_HEADER in call.request.read()


# -- api: чтение -------------------------------------------------------------


@respx.mock
def test_uploadings_path_and_params() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/7/offline_conversions/calls_uploadings"
    ).respond(json={"uploadings": []})
    with make_client() as c:
        Calls(c).uploadings(7, limit=10, offset=5)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["limit"] == "10"
    assert req.url.params["offset"] == "5"


@respx.mock
def test_uploading_path() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/7/offline_conversions/calls_uploading/99"
    ).respond(json={"uploading": {"id": 99}})
    with make_client() as c:
        payload = Calls(c).uploading(7, 99)
    assert route.called
    assert payload == {"uploading": {"id": 99}}


# -- CLI ---------------------------------------------------------------------


@respx.mock
def test_cli_upload_multipart(tmp_path: Path, monkeypatch) -> None:
    # токен нужен load_config при построении клиента в CLI-слое
    monkeypatch.setenv("METRIKA_TOKEN", "T")
    respx.post(
        f"{BASE}/management/v1/counter/42/offline_conversions/upload_calls"
    ).respond(json={"uploading": {"id": 1}})
    result = runner.invoke(
        app,
        [
            "calls",
            "upload",
            "42",
            "--file",
            write_csv(tmp_path),
            "--client-id-type",
            "CLIENT_ID",
            "--comment",
            "звонки за ноябрь",
        ],
    )
    assert result.exit_code == 0
    assert "multipart/form-data" in respx.calls[-1].request.headers["content-type"]
    assert respx.calls[-1].request.url.params["client_id_type"] == "CLIENT_ID"


def test_upload_requires_existing_file(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "calls",
            "upload",
            "42",
            "--file",
            str(tmp_path / "nope.csv"),
            "--client-id-type",
            "CLIENT_ID",
        ],
    )
    assert result.exit_code != 0
    assert "не найден" in result.output
