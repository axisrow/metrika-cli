"""Проверки группы expenses: multipart-upload/delete, delete_single, uploadings.

Офлайн: respx мокает transport; multipart-тело запроса разбирается по байтам.
"""

from pathlib import Path

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.expenses import Expenses
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

runner = CliRunner()
BASE = "https://api-metrika.yandex.net"

CSV_HEADER = b"Date,UTMSource,Expenses"


def make_client() -> Client:
    return Client(Config(token="T"))


def write_csv(tmp_path: Path) -> str:
    path = tmp_path / "expenses.csv"
    path.write_bytes(CSV_HEADER + b"\n2025-01-01,example.com,100.50\n")
    return str(path)


# -- registry -----------------------------------------------------------------


def test_expenses_endpoints() -> None:
    eps = registry.by_group(registry.ENDPOINTS, registry.GROUPS)["expenses"]
    assert [ep.op for ep in eps] == [
        "delete",
        "delete_single",
        "upload",
        "uploading",
        "uploadings",
    ]
    for op in ("upload", "delete"):
        ep = registry.get_endpoint("expenses", op)
        assert ep.method == "POST"
        assert ep.multipart is True


# -- api: multipart -----------------------------------------------------------


@respx.mock
def test_upload_multipart_body(tmp_path: Path) -> None:
    route = respx.post(f"{BASE}/management/v1/counter/42/expense/upload").respond(
        json={"uploading": {"id": 1, "status": "processing"}}
    )
    with make_client() as c:
        payload = Expenses(c).upload(42, write_csv(tmp_path), comment="crm dump")
    assert route.called
    assert payload == {"uploading": {"id": 1, "status": "processing"}}

    req = respx.calls[-1].request
    assert "multipart/form-data" in req.headers["content-type"]
    body = req.read()
    assert b'name="file"' in body
    assert b'filename="expenses.csv"' in body
    assert CSV_HEADER in body
    assert req.url.params["comment"] == "crm dump"
    assert "provider" not in req.url.params


@respx.mock
def test_upload_query_params(tmp_path: Path) -> None:
    respx.post(f"{BASE}/management/v1/counter/1/expense/upload").respond(
        json={"uploading": {}}
    )
    with make_client() as c:
        Expenses(c).upload(1, write_csv(tmp_path), provider="mycrm")
    assert respx.calls[-1].request.url.params["provider"] == "mycrm"


@respx.mock
def test_delete_multipart_body(tmp_path: Path) -> None:
    route = respx.post(f"{BASE}/management/v1/counter/42/expense/delete").respond(
        json={"uploading": {"id": 2, "status": "processing"}}
    )
    with make_client() as c:
        payload = Expenses(c).delete(42, write_csv(tmp_path))
    assert route.called
    assert payload == {"uploading": {"id": 2, "status": "processing"}}

    req = respx.calls[-1].request
    assert "multipart/form-data" in req.headers["content-type"]
    assert b'name="file"' in req.read()


# -- api: query-эндпоинты ------------------------------------------------------


@respx.mock
def test_delete_single_query() -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/42/expense/delete_single"
    ).respond(json={"uploading": {"id": 3}})
    with make_client() as c:
        payload = Expenses(c).delete_single(42, "2025-01-01", utm_campaign="promo")
    assert route.called
    assert payload == {"uploading": {"id": 3}}

    req = respx.calls[-1].request
    assert req.method == "POST"
    assert req.url.params["date"] == "2025-01-01"
    assert req.url.params["UTMCampaign"] == "promo"
    assert "provider" not in req.url.params


@respx.mock
def test_uploadings_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/expense/uploadings").respond(
        json={"uploadings": []}
    )
    with make_client() as c:
        payload = Expenses(c).uploadings(42, limit=10, offset=5)
    assert route.called
    assert payload == {"uploadings": []}

    req = respx.calls[-1].request
    assert req.url.params["limit"] == "10"
    assert req.url.params["offset"] == "5"


@respx.mock
def test_uploadings_defaults_omitted() -> None:
    respx.get(f"{BASE}/management/v1/counter/42/expense/uploadings").respond(
        json={"uploadings": []}
    )
    with make_client() as c:
        Expenses(c).uploadings(42)
    req = respx.calls[-1].request
    assert "limit" not in req.url.params
    assert "offset" not in req.url.params


@respx.mock
def test_uploading_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/expense/uploading/77").respond(
        json={"uploading": {"id": 77}}
    )
    with make_client() as c:
        payload = Expenses(c).uploading(42, 77)
    assert route.called
    assert payload == {"uploading": {"id": 77}}


# -- CLI (offline, CliRunner + respx) ------------------------------------------


def test_cli_expenses_help_lists_commands() -> None:
    from metrika_cli.commands import expenses as expenses_cli

    help_result = runner.invoke(expenses_cli.app, ["--help"])
    assert help_result.exit_code == 0
    for command in ("upload", "delete", "delete-single", "uploadings", "uploading"):
        assert command in help_result.output


@respx.mock
def test_cli_expenses_upload_e2e_offline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """CliRunner → команда → api → respx: полный прогон без сети."""
    from metrika_cli.cli import app as root_app

    csv_path = write_csv(tmp_path)
    monkeypatch.setenv("METRIKA_TOKEN", "T")
    route = respx.post(f"{BASE}/management/v1/counter/42/expense/upload").respond(
        json={"uploading": {"id": 9, "status": "processing"}}
    )
    result = runner.invoke(
        root_app,
        ["expenses", "upload", "42", "--file", csv_path, "--provider", "mycrm"],
    )
    assert result.exit_code == 0, result.output
    assert route.called
    assert respx.calls[-1].request.url.params["provider"] == "mycrm"
    assert "uploading" in result.output
