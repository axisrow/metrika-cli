"""Проверки группы conversions: multipart-upload, uploadings, uploading.

Офлайн: respx мокает transport; multipart-тело запроса разбирается по байтам.
"""

from pathlib import Path

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.conversions import Conversions
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

runner = CliRunner()
BASE = "https://api-metrika.yandex.net"

CSV_HEADER = b"ClientId,Target,Timestamp"


def make_client() -> Client:
    return Client(Config(token="T"))


def write_csv(tmp_path: Path) -> str:
    path = tmp_path / "conversions.csv"
    path.write_bytes(CSV_HEADER + b"\n123,https://ya.ru/,1481718246\n")
    return str(path)


# -- registry ---------------------------------------------------------------


def test_conversions_endpoints() -> None:
    eps = registry.by_group(registry.ENDPOINTS, registry.GROUPS)["conversions"]
    assert [ep.op for ep in eps] == ["upload", "uploading", "uploadings"]
    upload = registry.get_endpoint("conversions", "upload")
    assert upload.method == "POST"
    assert upload.multipart is True


# -- api: multipart ---------------------------------------------------------


@respx.mock
def test_upload_multipart_body(tmp_path: Path) -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/42/offline_conversions/upload"
    ).respond(json={"uploading": {"id": 1, "status": "processed"}})
    with make_client() as c:
        payload = Conversions(c).upload(42, write_csv(tmp_path), comment="crm dump")
    assert route.called
    assert payload == {"uploading": {"id": 1, "status": "processed"}}

    req = respx.calls[-1].request
    assert "multipart/form-data" in req.headers["content-type"]
    body = req.read()
    # файл уходит form-полем "file" с содержимым CSV, а не JSON-телом
    assert b'name="file"' in body
    assert b'filename="conversions.csv"' in body
    assert CSV_HEADER in body


@respx.mock
def test_upload_query_params(tmp_path: Path) -> None:
    respx.post(f"{BASE}/management/v1/counter/1/offline_conversions/upload").respond(
        json={"uploading": {}}
    )
    with make_client() as c:
        Conversions(c).upload(1, write_csv(tmp_path), comment="загрузка", type_="BASIC")
    req = respx.calls[-1].request
    assert req.url.params["comment"] == "загрузка"
    assert req.url.params["type"] == "BASIC"


# -- api: чтение ------------------------------------------------------------


@respx.mock
def test_uploadings_path_and_params() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/7/offline_conversions/uploadings"
    ).respond(json={"uploadings": []})
    with make_client() as c:
        Conversions(c).uploadings(7, limit=10, offset=5, type_="BASIC")
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["limit"] == "10"
    assert req.url.params["offset"] == "5"
    assert req.url.params["type"] == "BASIC"


@respx.mock
def test_uploading_path() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/7/offline_conversions/uploading/99"
    ).respond(json={"uploading": {"id": 99}})
    with make_client() as c:
        payload = Conversions(c).uploading(7, 99)
    assert route.called
    assert payload == {"uploading": {"id": 99}}


# -- CLI --------------------------------------------------------------------


def test_upload_requires_existing_file(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["conversions", "upload", "42", "--file", str(tmp_path / "nope.csv")]
    )
    assert result.exit_code != 0
    assert "не найден" in result.output
