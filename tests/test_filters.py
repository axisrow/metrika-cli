"""Проверки группы filters: реестр путей, api-ресурс (respx), CLI-команды."""

import json
from typing import Any

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.filters import Filters
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli import registry

runner = CliRunner()

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"

FILTER_BODY: Any = {
    "action": "exclude",
    "attr": "referrer",
    "type": "regexp",
    "value": r"\.example\.com",
}


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_filters_endpoints() -> None:
    expected = {
        ("list", "GET", "management/v1/counter/{counterId}/filters"),
        ("create", "POST", "management/v1/counter/{counterId}/filters"),
        ("get", "GET", "management/v1/counter/{counterId}/filter/{filterId}"),
        ("edit", "PUT", "management/v1/counter/{counterId}/filter/{filterId}"),
        ("delete", "DELETE", "management/v1/counter/{counterId}/filter/{filterId}"),
    }
    actual = {
        (ep.op, ep.method, ep.path) for ep in registry.GROUPED[registry.GROUP_FILTERS]
    }
    assert actual == expected


@respx.mock
def test_filters_list_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/filters").respond(
        json={"filters": []}
    )
    with make_client() as c:
        Filters(c).list(42)
    assert route.called


@respx.mock
def test_filter_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/filter/7").respond(
        json={"filter": {"id": 7}}
    )
    with make_client() as c:
        Filters(c).get(42, 7)
    assert route.called


@respx.mock
def test_filter_create_body() -> None:
    respx.post(f"{BASE}/management/v1/counter/42/filters").respond(
        json={"filter": {"id": 7}}
    )
    with make_client() as c:
        Filters(c).create(42, FILTER_BODY)
    request = respx.calls[-1].request
    assert json.loads(request.read()) == {"filter": FILTER_BODY}


@respx.mock
def test_filter_edit_body() -> None:
    respx.put(f"{BASE}/management/v1/counter/42/filter/7").respond(
        json={"filter": {"id": 7}}
    )
    with make_client() as c:
        Filters(c).edit(42, 7, FILTER_BODY)
    request = respx.calls[-1].request
    assert json.loads(request.read()) == {"filter": FILTER_BODY}


@respx.mock
def test_filter_delete_path() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/42/filter/7").respond(
        json={"success": True}
    )
    with make_client() as c:
        Filters(c).delete(42, 7)
    assert route.called


@respx.mock
def test_cli_filters_get() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/filter/7").respond(
        json={"filter": {"id": 7}}
    )
    result = runner.invoke(app, ["--token", "T", "filters", "get", "42", "7"])
    assert result.exit_code == 0
    assert route.called


@respx.mock
def test_cli_filters_create_data() -> None:
    respx.post(f"{BASE}/management/v1/counter/42/filters").respond(
        json={"filter": {"id": 7}}
    )
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "filters",
            "create",
            "42",
            "--data",
            json.dumps(FILTER_BODY),
        ],
    )
    assert result.exit_code == 0
    request = respx.calls[-1].request
    assert json.loads(request.read()) == {"filter": FILTER_BODY}
