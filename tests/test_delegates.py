"""Тесты группы delegates: registry-описания + api-слой (respx, offline)."""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.delegates import Delegates
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli import registry

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_delegates_paths() -> None:
    assert registry.get_endpoint("delegates", "list").path == "management/v1/delegates"
    assert (
        registry.get_endpoint("delegates", "create").path == "management/v1/delegates"
    )
    # по openapi deleteDelegate: путь без плейсхолдера, логин — query
    assert registry.get_endpoint("delegates", "delete").path == "management/v1/delegate"


@respx.mock
def test_delegates_list() -> None:
    route = respx.get(f"{BASE}/management/v1/delegates").respond(json={"delegates": []})
    with make_client() as c:
        Delegates(c).list()
    assert route.called


@respx.mock
def test_delegates_create_body() -> None:
    route = respx.post(f"{BASE}/management/v1/delegates").respond(
        json={"delegates": []}
    )
    with make_client() as c:
        Delegates(c).create({"user_login": "a"})
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"delegate": {"user_login": "a"}}


@respx.mock
def test_delegates_delete_query_param() -> None:
    route = respx.delete(f"{BASE}/management/v1/delegate").respond(
        json={"success": True}
    )
    with make_client() as c:
        Delegates(c).delete("somebody")
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["user_login"] == "somebody"


def test_cli_delegates_help_lists_commands() -> None:
    from metrika_cli.commands import delegates as delegates_cli

    runner = CliRunner()
    help_result = runner.invoke(delegates_cli.app, ["--help"])
    assert help_result.exit_code == 0
    for command in ("list", "create", "delete"):
        assert command in help_result.output


@respx.mock
def test_cli_delegates_delete_e2e_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    """CliRunner → команда → api → respx: полный прогон без сети."""
    from metrika_cli.commands.delegates import app as delegates_app

    monkeypatch.setenv("METRIKA_TOKEN", "T")
    route = respx.delete(f"{BASE}/management/v1/delegate").respond(
        json={"success": True}
    )
    runner = CliRunner()
    result = runner.invoke(delegates_app, ["delete", "somebody"])
    assert result.exit_code == 0, result.output
    assert route.called
    assert respx.calls[-1].request.url.params["user_login"] == "somebody"
    assert "success" in result.output
