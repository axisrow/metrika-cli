"""Проверки группы segments: пути registry, запросы api-ресурса, команды CLI."""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.segments import Segments
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli.registry import get_endpoint

# integration: файл смешивает unit-тесты registry и respx-проверки api/CLI,
# метка выбирает файл через -m integration (профиль остальных тестовых файлов)
pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"

SEGMENT = {"segmentId": "777", "name": "test", "expression": "ym:s:pageViews>=1"}


def make_client() -> Client:
    return Client(Config(token="T"))


# -- registry ----------------------------------------------------------------


def test_registry_paths() -> None:
    assert get_endpoint("segments", "list").path == (
        "management/v1/counter/{counterId}/apisegment/segments"
    )
    assert get_endpoint("segments", "list").method == "GET"
    assert get_endpoint("segments", "create").method == "POST"
    assert get_endpoint("segments", "get").path == (
        "management/v1/counter/{counterId}/apisegment/segment/{segmentId}"
    )
    assert get_endpoint("segments", "get").method == "GET"
    assert get_endpoint("segments", "edit").method == "PUT"
    assert get_endpoint("segments", "delete").method == "DELETE"


# -- api-ресурс (respx) -------------------------------------------------------


@respx.mock
def test_list_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/apisegment/segments").respond(
        json={"segments": []}
    )
    with make_client() as c:
        Segments(c).list(123)
    assert route.called


@respx.mock
def test_create_body_and_path() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/apisegment/segments").respond(
        json=SEGMENT
    )
    with make_client() as c:
        Segments(c).create(123, {"name": "test", "expression": "ym:s:pageViews>=1"})
    assert route.called
    body = json.loads(respx.calls[-1].request.content)
    assert body["segment"]["expression"] == "ym:s:pageViews>=1"


@respx.mock
def test_get_path() -> None:
    route = respx.get(
        f"{BASE}/management/v1/counter/123/apisegment/segment/777"
    ).respond(json=SEGMENT)
    with make_client() as c:
        Segments(c).get(123, "777")
    assert route.called


@respx.mock
def test_edit_method_and_body() -> None:
    route = respx.put(
        f"{BASE}/management/v1/counter/123/apisegment/segment/777"
    ).respond(json=SEGMENT)
    with make_client() as c:
        Segments(c).edit(123, "777", {"name": "renamed"})
    assert route.called
    assert respx.calls[-1].request.method == "PUT"
    body = json.loads(respx.calls[-1].request.content)
    assert body["segment"]["name"] == "renamed"


@respx.mock
def test_delete_method_and_path() -> None:
    route = respx.delete(
        f"{BASE}/management/v1/counter/123/apisegment/segment/777"
    ).respond(status_code=200)
    with make_client() as c:
        Segments(c).delete(123, "777")
    assert route.called
    assert respx.calls[-1].request.method == "DELETE"


# -- CLI (offline, CliRunner + respx) -----------------------------------------

runner = CliRunner()


@respx.mock
def test_cli_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/apisegment/segments").respond(
        json={"segments": [SEGMENT]}
    )
    result = runner.invoke(app, ["--token", "T", "segments", "list", "123"])
    assert result.exit_code == 0, result.output
    assert route.called
    assert '"segmentId": "777"' in result.output


@respx.mock
def test_cli_create() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/apisegment/segments").respond(
        json=SEGMENT
    )
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "segments",
            "create",
            "123",
            "--data",
            '{"name": "test", "expression": "ym:s:pageViews>=1"}',
        ],
    )
    assert result.exit_code == 0, result.output
    assert route.called
    assert '"name": "test"' in result.output


@respx.mock
def test_cli_delete() -> None:
    route = respx.delete(
        f"{BASE}/management/v1/counter/123/apisegment/segment/777"
    ).respond(status_code=200)
    result = runner.invoke(app, ["--token", "T", "segments", "delete", "123", "777"])
    assert result.exit_code == 0, result.output
    assert route.called
