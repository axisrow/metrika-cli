"""Проверки группы measurement: токены Measurement Protocol (issue #42).

Контракт сверен с официальным openapi
(management/openapi/measurement/{generateToken,deleteToken}.md, ревизия
r21770580): generate — GET без параметров; delete — POST, token —
обязательный query-параметр.
"""

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.measurement import Measurement
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli import registry

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_endpoints() -> None:
    gen = registry.get_endpoint("measurement", "generate")
    assert gen.method == "GET"
    assert gen.path == "management/v1/counter/{counterId}/measurement/generate"
    dele = registry.get_endpoint("measurement", "delete")
    assert dele.method == "POST"
    assert dele.path == "management/v1/counter/{counterId}/measurement/delete"


@respx.mock
def test_generate_get_without_params() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/measurement/generate").respond(
        json="123456abcdef"
    )
    with make_client() as c:
        Measurement(c).generate(123)
    assert route.called
    assert not respx.calls[-1].request.url.params


@respx.mock
def test_delete_token_is_query_param() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/measurement/delete").respond(
        json={"success": True}
    )
    with make_client() as c:
        Measurement(c).delete(123, "tok123")
    assert route.called
    assert respx.calls[-1].request.url.params["token"] == "tok123"
    assert respx.calls[-1].request.read() == b""


@respx.mock
def test_cli_generate() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/measurement/generate").respond(
        json="token123"
    )
    result = runner.invoke(app, ["--token", "T", "measurement", "generate", "123"])
    assert result.exit_code == 0
    assert route.called


@respx.mock
def test_cli_delete_passes_token() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/measurement/delete").respond(
        json={"success": True}
    )
    result = runner.invoke(
        app, ["--token", "T", "measurement", "delete", "123", "--token", "tok123"]
    )
    assert result.exit_code == 0
    assert route.called
    assert route.calls.last.request.url.params["token"] == "tok123"
