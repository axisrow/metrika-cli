"""Offline-тесты 6-й операции Reports API: comparison_drilldown (issue #34).

Путь и набор параметров сверены с openapi-справочником stat
(«Сравнение - drill down», stat/v1/data/comparison/drilldown).
"""

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.stat import Stat
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config
from metrika_cli import registry

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"
PATH = f"{BASE}/stat/v1/data/comparison/drilldown"


def make_client() -> Client:
    return Client(Config(token="T"))


def test_registry_endpoint() -> None:
    ep = registry.get_endpoint("stat", "comparison_drilldown")
    assert ep.method == "GET"
    assert ep.path == "stat/v1/data/comparison/drilldown"


@respx.mock
def test_path_and_required_params() -> None:
    route = respx.get(PATH).respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).comparison_drilldown(ids="44147844", metrics="ym:s:visits")
    assert route.called
    req = respx.calls[-1].request
    assert req.url.params["ids"] == "44147844"
    assert req.url.params["metrics"] == "ym:s:visits"
    # ни один опциональный параметр не должен просачиваться как пустой
    assert "parent_id" not in req.url.params
    assert "date1_a" not in req.url.params


@respx.mock
def test_ab_and_tree_params() -> None:
    route = respx.get(PATH).respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).comparison_drilldown(
            ids="44147844",
            metrics="ym:s:visits",
            dimensions="ym:s:operatingSystem",
            date1_a="2026-01-01",
            date2_a="2026-01-31",
            date1_b="2025-01-01",
            date2_b="2025-01-31",
            filters_a="ym:s:pageViews>5",
            filters_b="ym:s:pageViews>10",
            parent_id="",
            limit=10,
        )
    assert route.called
    params = respx.calls[-1].request.url.params
    assert params["date1_a"] == "2026-01-01"
    assert params["date2_b"] == "2025-01-31"
    assert params["filters_a"] == "ym:s:pageViews>5"
    assert params["parent_id"] == ""
    assert params["limit"] == "10"
    assert "date1" not in params  # базовые date1/date2 не в сигнатуре метода


@respx.mock
def test_csv_suffix() -> None:
    route = respx.get(url=f"{PATH}.csv").respond(content=b"a,b")
    with make_client() as c:
        text = Stat(c).comparison_drilldown(ids="1", metrics="ym:s:visits", csv=True)
    assert route.called
    assert text == "a,b"


@respx.mock
def test_cli_comparison_drilldown() -> None:
    route = respx.get(PATH).respond(
        json={
            "total_rows": 1,
            "data": [
                {
                    "dimensions": [{"name": "macOS"}],
                    "metrics": [{"a": 10.0, "b": 20.0}],
                }
            ],
        }
    )
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "stat",
            "comparison-drilldown",
            "--ids",
            "44147844",
            "--metrics",
            "ym:s:visits",
            "--date1-a",
            "2026-01-01",
            "--date2-b",
            "2025-01-31",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    req = route.calls.last.request
    assert req.url.params["date1_a"] == "2026-01-01"
    assert req.url.params["date2_b"] == "2025-01-31"
    assert '"total_rows": 1' in result.output
