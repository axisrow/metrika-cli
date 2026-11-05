"""Проверки группы clients: клиенты Директа (issue #42).

Контракт сверен с официальным openapi
(management/openapi/clients/getClients.md, ревизия r21770580):
GET /management/v1/clients?counters=... — counters обязателен, ID через
запятую; ответ {"clients": [{id, chief_login, ...}]}.
"""

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.clients import Clients
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli import registry

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
PATH = f"{BASE}/management/v1/clients"

runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_endpoint() -> None:
    ep = registry.get_endpoint("clients", "list")
    assert ep.method == "GET"
    assert ep.path == "management/v1/clients"


@respx.mock
def test_list_counters_required_query_param() -> None:
    respx.get(PATH).respond(json={"clients": [{"id": 1, "chief_login": "chief"}]})
    with make_client() as c:
        Clients(c).list("111,222")
    assert respx.calls[-1].request.url.params["counters"] == "111,222"


@respx.mock
def test_cli_list() -> None:
    route = respx.get(PATH).respond(json={"clients": [{"id": 1}]})
    result = runner.invoke(app, ["--token", "T", "clients", "list", "--counters", "111,222"])
    assert result.exit_code == 0
    assert route.called
    assert route.calls.last.request.url.params["counters"] == "111,222"


def test_cli_list_requires_counters() -> None:
    result = runner.invoke(app, ["--token", "T", "clients", "list"])
    assert result.exit_code != 0
