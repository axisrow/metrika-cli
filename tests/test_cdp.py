"""Проверки группы cdp — загрузки клиентов/заказов (issue #42).

Контракт сверен с официальным openapi
(management/openapi/schema/{uploadContacts,uploadContactJson_1,uploadOrders,
uploadOrdersJson_1,uploadSimpleOrders,getLastUploadings}.md, ревизия
r21770580): префикс /cdp/api/v1; CSV — multipart + columns_mapping/
merge_mode (обязательные), delimiter_type; JSON — тело {"contacts"/"orders"}.
"""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.cdp import Cdp
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
CDP = f"{BASE}/cdp/api/v1/counter/123"

runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


def make_csv(tmp_path) -> str:
    path = tmp_path / "rows.csv"
    path.write_text("uniq_id,name\n1,alice\n", encoding="utf-8")
    return str(path)


@respx.mock
def test_upload_contacts_csv_multipart_and_query(tmp_path) -> None:
    respx.post(f"{CDP}/data/contacts/csv").respond(json={})
    with make_client() as c:
        Cdp(c).upload_contacts(
            123,
            make_csv(tmp_path),
            columns_mapping="uniq_id,name",
            merge_mode="APPEND",
            delimiter_type="SEMICOLON",
        )
    req = respx.calls[-1].request
    assert req.url.params["columns_mapping"] == "uniq_id,name"
    assert req.url.params["merge_mode"] == "APPEND"
    assert req.url.params["delimiter_type"] == "SEMICOLON"
    assert b'name="file"' in req.read()


@respx.mock
def test_upload_contacts_json_body(tmp_path) -> None:
    respx.post(f"{CDP}/data/contacts/json").respond(json={})
    with make_client() as c:
        Cdp(c).upload_contacts_json(
            123, {"contacts": [{"uniq_id": "1"}]}, merge_mode="SAVE"
        )
    req = respx.calls[-1].request
    assert req.url.params["merge_mode"] == "SAVE"
    assert json.loads(req.read()) == {"contacts": [{"uniq_id": "1"}]}


@respx.mock
def test_upload_orders_csv_multipart_and_query(tmp_path) -> None:
    respx.post(f"{CDP}/data/orders/csv").respond(json={})
    with make_client() as c:
        Cdp(c).upload_orders(
            123,
            make_csv(tmp_path),
            columns_mapping="id,order_status",
            merge_mode="APPEND",
        )
    req = respx.calls[-1].request
    assert req.url.params["columns_mapping"] == "id,order_status"
    assert req.url.params["merge_mode"] == "APPEND"
    assert "delimiter_type" not in req.url.params
    assert b'name="file"' in req.read()


@respx.mock
def test_upload_orders_json_body(tmp_path) -> None:
    respx.post(f"{CDP}/data/orders/json").respond(json={})
    with make_client() as c:
        Cdp(c).upload_orders_json(
            123, {"orders": [{"id": "ord1", "client_uniq_id": "1"}]}, merge_mode="APPEND"
        )
    req = respx.calls[-1].request
    assert json.loads(req.read()) == {"orders": [{"id": "ord1", "client_uniq_id": "1"}]}


@respx.mock
def test_upload_simple_orders_multipart(tmp_path) -> None:
    respx.post(f"{CDP}/data/simple_orders").respond(json={})
    with make_client() as c:
        Cdp(c).upload_simple_orders(123, make_csv(tmp_path), merge_mode="SAVE")
    req = respx.calls[-1].request
    assert req.url.params["merge_mode"] == "SAVE"
    assert "columns_mapping" not in req.url.params
    assert b'name="file"' in req.read()


@respx.mock
def test_last_uploadings_query_params() -> None:
    respx.get(f"{CDP}/last_uploadings").respond(json={"uploadings": []})
    with make_client() as c:
        Cdp(c).last_uploadings(
            123, datetime_offset="2026-01-01 00:00:00", limit=10, source="API"
        )
    params = respx.calls[-1].request.url.params
    assert params["datetime_offset"] == "2026-01-01 00:00:00"
    assert params["limit"] == "10"
    assert params["source"] == "API"


@respx.mock
def test_cli_upload_contacts_csv(tmp_path) -> None:
    route = respx.post(f"{CDP}/data/contacts/csv").respond(json={})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "upload-contacts",
            "123",
            "--file",
            make_csv(tmp_path),
            "--columns-mapping",
            "uniq_id,name",
            "--merge-mode",
            "APPEND",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    params = route.calls.last.request.url.params
    assert params["columns_mapping"] == "uniq_id,name"
    assert params["merge_mode"] == "APPEND"


@respx.mock
def test_cli_upload_accepts_merge_mode_update(tmp_path) -> None:
    """UPDATE — третье документированное значение merge_mode (issue #42 ревью)."""
    respx.post(f"{CDP}/data/simple_orders").respond(json={})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "upload-simple-orders",
            "123",
            "--file",
            make_csv(tmp_path),
            "--merge-mode",
            "UPDATE",
        ],
    )
    assert result.exit_code == 0
    assert respx.calls[-1].request.url.params["merge_mode"] == "UPDATE"


@respx.mock
def test_cli_upload_contacts_json_wraps_list() -> None:
    respx.post(f"{CDP}/data/contacts/json").respond(json={})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "upload-contacts-json",
            "123",
            "--data",
            '[{"uniq_id": "1"}]',
            "--merge-mode",
            "SAVE",
        ],
    )
    assert result.exit_code == 0
    assert json.loads(respx.calls[-1].request.read()) == {
        "contacts": [{"uniq_id": "1"}]
    }


@respx.mock
def test_cli_upload_orders_json_object_passthrough() -> None:
    respx.post(f"{CDP}/data/orders/json").respond(json={})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "upload-orders-json",
            "123",
            "--data",
            '{"orders": [{"id": "a"}]}',
            "--merge-mode",
            "APPEND",
        ],
    )
    assert result.exit_code == 0
    assert json.loads(respx.calls[-1].request.read()) == {"orders": [{"id": "a"}]}


@respx.mock
def test_cli_last_uploadings() -> None:
    respx.get(f"{CDP}/last_uploadings").respond(json={"uploadings": []})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "last-uploadings",
            "123",
            "--limit",
            "10",
            "--source",
            "API",
        ],
    )
    assert result.exit_code == 0
    params = respx.calls[-1].request.url.params
    assert params["limit"] == "10"
    assert params["source"] == "API"


def test_cli_upload_missing_file_rejected(tmp_path) -> None:
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "cdp",
            "upload-contacts",
            "123",
            "--file",
            str(tmp_path / "nope.csv"),
            "--columns-mapping",
            "a,b",
            "--merge-mode",
            "APPEND",
        ],
    )
    assert result.exit_code != 0
