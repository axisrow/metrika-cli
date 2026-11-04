"""Проверки группы annotations: api-слой через respx + прогон CLI-команд."""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.annotations import Annotations
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
ANNOTATION = {"date": "2025-01-01", "time": "12:00:00", "title": "launch", "group": "A"}

runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_list_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/chart_annotations").respond(
        json={"chart_annotations": [ANNOTATION]}
    )
    with make_client() as c:
        data = Annotations(c).list(42)
    assert route.called
    assert data == {"chart_annotations": [ANNOTATION]}


@respx.mock
def test_create_body_wrapped() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/42/chart_annotations").respond(
        json={"chart_annotation": ANNOTATION}
    )
    with make_client() as c:
        Annotations(c).create(42, ANNOTATION)
    assert route.called
    sent = json.loads(route.calls.last.request.content)
    assert sent == {"chart_annotation": ANNOTATION}


@respx.mock
def test_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/chart_annotation/7").respond(
        json={"chart_annotation": {**ANNOTATION, "id": 7}}
    )
    with make_client() as c:
        Annotations(c).get(42, 7)
    assert route.called


@respx.mock
def test_edit_method_and_body() -> None:
    route = respx.put(f"{BASE}/management/v1/counter/42/chart_annotation/7").respond(
        json={"chart_annotation": {**ANNOTATION, "id": 7}}
    )
    with make_client() as c:
        Annotations(c).edit(42, 7, ANNOTATION)
    assert route.called
    request = route.calls.last.request
    assert request.method == "PUT"
    assert json.loads(request.content) == {"chart_annotation": ANNOTATION}


@respx.mock
def test_delete_path() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/42/chart_annotation/7").respond(
        json={"success": True}
    )
    with make_client() as c:
        Annotations(c).delete(42, 7)
    assert route.called


@respx.mock
def test_cli_get() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/42/chart_annotation/7").respond(
        json={"chart_annotation": {**ANNOTATION, "id": 7}}
    )
    result = runner.invoke(app, ["--token", "T", "annotations", "get", "42", "7"])
    assert result.exit_code == 0
    assert route.called
    assert '"id": 7' in result.output


@respx.mock
def test_cli_create_via_stdin() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/42/chart_annotations").respond(
        json={"chart_annotation": ANNOTATION}
    )
    result = runner.invoke(
        app,
        ["--token", "T", "annotations", "create", "42", "--data", "-"],
        input=json.dumps(ANNOTATION),
    )
    assert result.exit_code == 0
    assert route.called
    sent = json.loads(route.calls.last.request.content)
    assert sent == {"chart_annotation": ANNOTATION}
