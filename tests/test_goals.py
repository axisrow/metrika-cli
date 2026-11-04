"""Интеграционные проверки группы goals: api-ресурс и CLI-команды (respx)."""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.goals import Goals
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"

runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_goals_list_path_and_params() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/goals").respond(
        json={"goals": []}
    )
    with make_client() as c:
        Goals(c).list(123, use_deleted=True)
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["useDeleted"] == "true"


@respx.mock
def test_goals_list_default_no_deleted() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/goals").respond(
        json={"goals": []}
    )
    with make_client() as c:
        Goals(c).list(123)
    assert route.called
    assert respx.calls[-1].request.url.params["useDeleted"] == "false"


@respx.mock
def test_goal_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/goal/45").respond(
        json={"goal": {}}
    )
    with make_client() as c:
        Goals(c).get(123, 45)
    assert route.called


@respx.mock
def test_goals_create_wraps_body() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/goals").respond(
        json={"goal": {"id": 1}}
    )
    with make_client() as c:
        Goals(c).create(123, {"name": "цель"})
    assert route.called
    assert json.loads(respx.calls[-1].request.content) == {"goal": {"name": "цель"}}


@respx.mock
def test_goal_edit_path_and_body() -> None:
    route = respx.put(f"{BASE}/management/v1/counter/123/goal/45").respond(
        json={"goal": {"id": 45}}
    )
    with make_client() as c:
        Goals(c).edit(123, 45, {"name": "новая"})
    assert route.called
    assert json.loads(respx.calls[-1].request.content) == {"goal": {"name": "новая"}}


@respx.mock
def test_goal_delete_path() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/goal/45").respond(
        json={"success": True}
    )
    with make_client() as c:
        Goals(c).delete(123, 45)
    assert route.called


@respx.mock
def test_cli_goals_list_use_deleted_flag() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/7/goals").respond(
        json={"goals": []}
    )
    result = runner.invoke(app, ["--token", "T", "goals", "list", "7", "--use-deleted"])
    assert result.exit_code == 0
    assert route.called
    assert respx.calls[-1].request.url.params["useDeleted"] == "true"


@respx.mock
def test_cli_goals_create_data_option() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/7/goals").respond(
        json={"goal": {"id": 1}}
    )
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "goals",
            "create",
            "7",
            "--data",
            '{"name": "x", "type": "url", "conditions": []}',
        ],
    )
    assert result.exit_code == 0
    assert route.called
    assert json.loads(respx.calls[-1].request.content) == {
        "goal": {"name": "x", "type": "url", "conditions": []}
    }
