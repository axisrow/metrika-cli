"""Проверки группы counters: undelete и query-параметры list/get/create/edit.

Параметры сверены с официальным openapi
(management/openapi/counter/{counters,counter,addCounter,editCounter,
undeleteCounter}.md, ревизия r21770580, 2026-11-05).
"""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.counters import Counters
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
LIST = f"{BASE}/management/v1/counters"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_list_filter_params() -> None:
    respx.get(LIST).respond(json={"rows": 0, "counters": []})
    with make_client() as c:
        Counters(c).list(
            counter_ids="1,2,3",
            favorite=True,
            field="goals,grants",
            label_id=5,
            permission="own,edit",
            reverse=True,
            robots=False,
            search_string="shop",
            sort="Visits",
            status="Active",
            type="simple",
        )
    params = respx.calls[-1].request.url.params
    assert params["counter_ids"] == "1,2,3"
    assert params["favorite"] == "true"
    assert params["field"] == "goals,grants"
    assert params["label_id"] == "5"
    assert params["permission"] == "own,edit"
    assert params["reverse"] == "true"
    assert params["robots"] == "false"
    assert params["search_string"] == "shop"
    assert params["sort"] == "Visits"
    assert params["status"] == "Active"
    assert params["type"] == "simple"


@respx.mock
def test_list_filters_absent_do_not_leak() -> None:
    respx.get(LIST).respond(json={"rows": 0, "counters": []})
    with make_client() as c:
        Counters(c).list()
    assert dict(respx.calls[-1].request.url.params) == {"offset": "1"}


@respx.mock
def test_get_and_edit_field_param() -> None:
    get_route = respx.get(f"{BASE}/management/v1/counter/123").respond(json={})
    edit_route = respx.put(f"{BASE}/management/v1/counter/123").respond(json={})
    with make_client() as c:
        Counters(c).get(123, field="goals,mirrors")
        Counters(c).edit(123, {"name": "x"}, field="goals")
    assert get_route.called
    assert respx.calls[0].request.url.params["field"] == "goals,mirrors"
    assert edit_route.called
    assert respx.calls[1].request.url.params["field"] == "goals"


@respx.mock
def test_create_field_and_ytm() -> None:
    respx.post(LIST).respond(json={})
    with make_client() as c:
        Counters(c).create({"name": "x", "site": "example.com"}, field="goals", ytm=True)
    params = respx.calls[-1].request.url.params
    assert params["field"] == "goals"
    assert params["ytm"] == "true"


@respx.mock
def test_undelete_posts_to_undelete_path() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/undelete").respond(
        json={"success": True}
    )
    with make_client() as c:
        Counters(c).undelete(123)
    assert route.called
    assert respx.calls[-1].request.read() == b""


@respx.mock
def test_registry_undelete_endpoint() -> None:
    from metrika_cli import registry

    ep = registry.get_endpoint("counters", "undelete")
    assert ep.method == "POST"
    assert ep.path == "management/v1/counter/{counterId}/undelete"


@respx.mock
def test_cli_list_filters() -> None:
    respx.get(LIST).respond(json={"rows": 0, "counters": []})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "counters",
            "list",
            "--counter-ids",
            "1,2",
            "--favorite",
            "--field",
            "goals",
            "--label-id",
            "5",
            "--permission",
            "own",
            "--reverse",
            "--no-robots",
            "--search-string",
            "shop",
            "--sort",
            "Visits",
            "--status",
            "Active",
            "--type",
            "simple",
        ],
    )
    assert result.exit_code == 0
    params = respx.calls[-1].request.url.params
    assert params["counter_ids"] == "1,2"
    assert params["favorite"] == "true"
    assert params["field"] == "goals"
    assert params["label_id"] == "5"
    assert params["permission"] == "own"
    assert params["reverse"] == "true"
    assert params["robots"] == "false"
    assert params["search_string"] == "shop"
    assert params["sort"] == "Visits"
    assert params["status"] == "Active"
    assert params["type"] == "simple"


@respx.mock
def test_cli_undelete() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/undelete").respond(
        json={"success": True}
    )
    runner = CliRunner()
    result = runner.invoke(app, ["--token", "T", "counters", "undelete", "123"])
    assert result.exit_code == 0
    assert route.called
    assert json.loads(result.output) == {"success": True}


@respx.mock
def test_cli_create_field_ytm() -> None:
    respx.post(LIST).respond(json={})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "counters",
            "create",
            "--data",
            '{"name":"x","site":"example.com"}',
            "--field",
            "goals",
            "--ytm",
        ],
    )
    assert result.exit_code == 0
    params = respx.calls[-1].request.url.params
    assert params["field"] == "goals"
    assert params["ytm"] == "true"


@respx.mock
def test_cli_get_field() -> None:
    respx.get(f"{BASE}/management/v1/counter/123").respond(json={"id": 123})
    runner = CliRunner()
    result = runner.invoke(
        app, ["--token", "T", "counters", "get", "123", "--field", "goals"]
    )
    assert result.exit_code == 0
    assert respx.calls[-1].request.url.params["field"] == "goals"
