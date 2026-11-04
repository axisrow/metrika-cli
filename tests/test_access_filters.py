"""Offline-проверки access_filters: пути реестра, api-слой, команды CLI.

Пути сняты с официальных openapi-страниц (issue 18, investigation-first):
- GET/POST  management/v1/counter/{counterId}/access_filters
- GET/PUT/DELETE management/v1/counter/{counterId}/access_filter/{accessFilterId}
"""

import json

import respx
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.api.access_filters import AccessFilters
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

runner = CliRunner()

BASE = "https://api-metrika.yandex.net"

FILTER = {"id": 7, "attr": " referral_source", "type": "exclude", "value": "spam"}


def make_client() -> Client:
    return Client(Config(token="T"))


def cli(args: list[str]):
    return runner.invoke(app, ["--token", "T", *args])


# --- registry: пути ровно как в openapi -------------------------------------


def test_registry_paths() -> None:
    expected = {
        "list": ("GET", "management/v1/counter/{counterId}/access_filters"),
        "create": ("POST", "management/v1/counter/{counterId}/access_filters"),
        "get": (
            "GET",
            "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
        ),
        "edit": (
            "PUT",
            "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
        ),
        "delete": (
            "DELETE",
            "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
        ),
    }
    for op, (method, path) in expected.items():
        ep = registry.get_endpoint("access_filters", op)
        assert ep.method == method
        assert ep.path == path


# --- api-слой ---------------------------------------------------------------


@respx.mock
def test_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/access_filters").respond(
        json={"access_filters": [FILTER]}
    )
    with make_client() as c:
        data = AccessFilters(c).list(42)
    assert route.called
    assert data["access_filters"] == [FILTER]


@respx.mock
def test_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/access_filter/7").respond(
        json={"access_filter": FILTER}
    )
    with make_client() as c:
        data = AccessFilters(c).get(42, 7)
    assert route.called
    assert data["access_filter"] == FILTER


@respx.mock
def test_create_body() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/42/access_filters").respond(
        json={"access_filter": FILTER}
    )
    with make_client() as c:
        AccessFilters(c).create(42, FILTER)
    assert route.called
    sent = json.loads(respx.calls[-1].request.content)
    assert sent == {"access_filter": FILTER}


@respx.mock
def test_edit_path_and_body() -> None:
    route = respx.put(f"{BASE}/management/v1/counter/42/access_filter/7").respond(
        json={"access_filter": FILTER}
    )
    updated = {**FILTER, "type": "include"}
    with make_client() as c:
        AccessFilters(c).edit(42, 7, updated)
    assert route.called
    sent = json.loads(respx.calls[-1].request.content)
    assert sent == {"access_filter": updated}


@respx.mock
def test_delete_default_keeps_grants() -> None:
    # Дефолт консервативный: связанные гранты не трогаем (delete_grants=false).
    route = respx.delete(f"{BASE}/management/v1/counter/42/access_filter/7").respond(
        json={"success": True}
    )
    with make_client() as c:
        AccessFilters(c).delete(42, 7)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["delete_grants"] == "false"


@respx.mock
def test_delete_with_grants() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/42/access_filter/7").respond(
        json={"success": True}
    )
    with make_client() as c:
        AccessFilters(c).delete(42, 7, delete_grants=True)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["delete_grants"] == "true"


# --- команды CLI ------------------------------------------------------------


@respx.mock
def test_cli_list() -> None:
    respx.get(f"{BASE}/management/v1/counter/42/access_filters").respond(
        json={"access_filters": [FILTER]}
    )
    result = cli(["access_filters", "list", "42"])
    assert result.exit_code == 0, result.output
    assert '"id": 7' in result.output or '"id":7' in result.output


@respx.mock
def test_cli_delete_flag() -> None:
    respx.delete(f"{BASE}/management/v1/counter/42/access_filter/7").respond(
        json={"success": True}
    )
    result = cli(["access_filters", "delete", "42", "7", "--delete-grants"])
    assert result.exit_code == 0, result.output
    req = respx.calls[-1].request
    assert req.url.params["delete_grants"] == "true"
