"""Интеграционные проверки группы expenses: api-ресурс строит правильный запрос."""

from pathlib import Path

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.expenses import Expenses
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"

CSV = b"Date,UTMSource,Expenses\n2025-01-01,example.com,100.50\n"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_expense_upload_multipart_and_query() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/expense/upload").respond(
        json={"uploading": {"id": 1}}
    )
    with make_client() as c:
        Expenses(c).upload(123, "exp.csv", CSV, comment="загрузка", provider="mycrm")
    assert route.called
    req = respx.calls[-1].request
    assert req.headers["content-type"].startswith("multipart/form-data")
    assert req.url.params["comment"] == "загрузка"
    assert req.url.params["provider"] == "mycrm"
    assert b"UTMSource" in req.content


@respx.mock
def test_expense_upload_drops_empty_query() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/expense/upload").respond(
        json={"uploading": {"id": 1}}
    )
    with make_client() as c:
        Expenses(c).upload(123, "exp.csv", CSV)
    assert route.called
    req = respx.calls[-1].request
    assert "comment" not in req.url.params
    assert "provider" not in req.url.params


@respx.mock
def test_expense_delete_multipart() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/expense/delete").respond(
        json={"uploading": {"id": 2}}
    )
    with make_client() as c:
        Expenses(c).delete(123, "del.csv", CSV, provider="mycrm")
    assert route.called
    req = respx.calls[-1].request
    assert req.headers["content-type"].startswith("multipart/form-data")
    assert req.url.params["provider"] == "mycrm"


@respx.mock
def test_expense_delete_single_query() -> None:
    route = respx.post(
        f"{BASE}/management/v1/counter/123/expense/delete_single"
    ).respond(json={"uploading": {"id": 3}})
    with make_client() as c:
        Expenses(c).delete_single(123, "2025-01-01", utm_campaign="promo")
    assert route.called
    req = respx.calls[-1].request
    assert req.method == "POST"
    assert req.url.params["date"] == "2025-01-01"
    assert req.url.params["UTMCampaign"] == "promo"
    assert "provider" not in req.url.params


@respx.mock
def test_expense_uploadings_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/expense/uploadings").respond(
        json={"uploadings": []}
    )
    with make_client() as c:
        Expenses(c).list(123, limit=10, offset=5)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["limit"] == "10"
    assert req.url.params["offset"] == "5"


@respx.mock
def test_expense_uploadings_list_defaults_omitted() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/expense/uploadings").respond(
        json={"uploadings": []}
    )
    with make_client() as c:
        Expenses(c).list(123)
    assert route.called
    req = respx.calls[-1].request
    assert "limit" not in req.url.params
    assert "offset" not in req.url.params


@respx.mock
def test_expense_uploading_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/expense/uploading/77").respond(
        json={"uploading": {"id": 77}}
    )
    with make_client() as c:
        Expenses(c).get(123, 77)
    assert route.called


# -- CLI (offline, CliRunner + respx) ------------------------------------------


def test_cli_expenses_help_lists_commands() -> None:
    from metrika_cli.commands import expenses as expenses_cli

    runner = CliRunner()
    help_result = runner.invoke(expenses_cli.app, ["--help"])
    assert help_result.exit_code == 0
    for command in ("upload", "delete", "delete-single", "list", "get"):
        assert command in help_result.output


@respx.mock
def test_cli_expenses_upload_e2e_offline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """CliRunner → команда → api → respx: полный прогон без сети."""
    from metrika_cli.commands.expenses import app as expenses_app

    csv_path = tmp_path / "exp.csv"
    csv_path.write_bytes(CSV)
    monkeypatch.setenv("METRIKA_TOKEN", "T")
    route = respx.post(f"{BASE}/management/v1/counter/123/expense/upload").respond(
        json={"uploading": {"id": 9, "status": "processing"}}
    )
    runner = CliRunner()
    result = runner.invoke(
        expenses_app,
        ["upload", "123", "--file", str(csv_path), "--provider", "mycrm"],
    )
    assert result.exit_code == 0, result.output
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["provider"] == "mycrm"
    assert b"Expenses" in req.content
    assert "uploading" in result.output
