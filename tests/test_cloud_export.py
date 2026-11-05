"""Проверки группы export: экспорт в Yandex Cloud (issue #42).

Контракт сверен с официальным openapi
(management/openapi/cloud/{getExportsByCounter,removeCounter}.md, ревизия
r21770580): префикс /export/v1, НЕ management.
"""

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.export import CloudExport
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
    lst = registry.get_endpoint("export", "list")
    assert lst.method == "GET"
    assert lst.path == "export/v1/cloud/counter/{counterId}"
    dele = registry.get_endpoint("export", "delete")
    assert dele.method == "DELETE"
    assert dele.path == "export/v1/cloud/{ceId}/counter/{counterId}"


@respx.mock
def test_list_uses_export_prefix() -> None:
    route = respx.get(f"{BASE}/export/v1/cloud/counter/123").respond(
        json={"cloud_export": []}
    )
    with make_client() as c:
        CloudExport(c).list(123)
    assert route.called


@respx.mock
def test_delete_path_has_ce_id_and_counter() -> None:
    route = respx.delete(f"{BASE}/export/v1/cloud/55/counter/123").respond(
        json={"success": True}
    )
    with make_client() as c:
        CloudExport(c).delete(55, 123)
    assert route.called


@respx.mock
def test_cli_list() -> None:
    route = respx.get(f"{BASE}/export/v1/cloud/counter/123").respond(
        json={"cloud_export": []}
    )
    result = runner.invoke(app, ["--token", "T", "export", "list", "123"])
    assert result.exit_code == 0
    assert route.called


@respx.mock
def test_cli_delete() -> None:
    route = respx.delete(f"{BASE}/export/v1/cloud/55/counter/123").respond(
        json={"success": True}
    )
    result = runner.invoke(app, ["--token", "T", "export", "delete", "55", "123"])
    assert result.exit_code == 0
    assert route.called
