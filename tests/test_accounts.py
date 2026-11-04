"""Тесты группы accounts: registry-описания + api-слой (respx, offline)."""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.accounts import Accounts
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_accounts_paths() -> None:
    assert registry.get_endpoint("accounts", "list").path == "management/v1/accounts"
    # update/delete отсутствуют в issue #6, добавлены по текущему openapi
    assert registry.get_endpoint("accounts", "update").path == "management/v1/accounts"
    # по openapi deleteAccount: путь единственного числа без плейсхолдера
    assert registry.get_endpoint("accounts", "delete").path == "management/v1/account"
    assert registry.get_endpoint("accounts", "update").method == "PUT"


@respx.mock
def test_accounts_list() -> None:
    route = respx.get(f"{BASE}/management/v1/accounts").respond(json={"accounts": []})
    with make_client() as c:
        Accounts(c).list()
    assert route.called


@respx.mock
def test_accounts_update_body() -> None:
    route = respx.put(f"{BASE}/management/v1/accounts").respond(json={"accounts": []})
    with make_client() as c:
        Accounts(c).update([{"user_login": "a"}])
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"accounts": [{"user_login": "a"}]}


@respx.mock
def test_accounts_delete_query_param() -> None:
    route = respx.delete(f"{BASE}/management/v1/account").respond(
        json={"success": True}
    )
    with make_client() as c:
        Accounts(c).delete("somebody")
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["user_login"] == "somebody"


@respx.mock
def test_cli_accounts_list_e2e_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    """CliRunner → команда → api → respx: полный прогон без сети."""
    from metrika_cli.commands.accounts import app as accounts_app

    monkeypatch.setenv("METRIKA_TOKEN", "T")
    route = respx.get(f"{BASE}/management/v1/accounts").respond(
        json={"accounts": [{"user_login": "a"}]}
    )
    runner = CliRunner()
    result = runner.invoke(accounts_app, ["list"])
    assert result.exit_code == 0, result.output
    assert route.called
    assert "user_login" in result.output
