"""Недостающие query-параметры отчётов (issue #42).

Наборы параметров для каждой из 6 операций сверены с openapi-справочником
stat (accuracy, proposed_accuracy, timezone, include_undefined,
direct_client_logins — общие; top_keys/row_ids/include_annotations/
annotation_groups/keys_sort — bytime; pivot_limit/pivot_offset — pivot;
only_expandable_undefined — drilldown и comparison_drilldown).
"""

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.stat import Stat
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_table_common_params() -> None:
    respx.get(f"{BASE}/stat/v1/data").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).table(
            ids="1",
            metrics="ym:s:visits",
            accuracy="high",
            proposed_accuracy=True,
            timezone="+03:00",
            include_undefined=True,
            direct_client_logins="login1,login2",
        )
    params = respx.calls[-1].request.url.params
    assert params["accuracy"] == "high"
    assert params["proposed_accuracy"] == "true"
    assert params["timezone"] == "+03:00"
    assert params["include_undefined"] == "true"
    assert params["direct_client_logins"] == "login1,login2"


@respx.mock
def test_table_common_params_absent_do_not_leak() -> None:
    respx.get(f"{BASE}/stat/v1/data").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).table(ids="1", metrics="ym:s:visits")
    params = respx.calls[-1].request.url.params
    for name in (
        "accuracy",
        "proposed_accuracy",
        "timezone",
        "include_undefined",
        "direct_client_logins",
    ):
        assert name not in params


@respx.mock
def test_bytime_specific_params() -> None:
    respx.get(f"{BASE}/stat/v1/data/bytime").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).bytime(
            ids="1",
            metrics="ym:s:visits",
            top_keys="10",
            row_ids="[[1],[2]]",
            include_annotations=True,
            annotation_groups="all",
            keys_sort="-ym:s:visits",
        )
    params = respx.calls[-1].request.url.params
    assert params["top_keys"] == "10"
    assert params["row_ids"] == "[[1],[2]]"
    assert params["include_annotations"] == "true"
    assert params["annotation_groups"] == "all"
    assert params["keys_sort"] == "-ym:s:visits"


@respx.mock
def test_pivot_limit_offset() -> None:
    respx.get(f"{BASE}/stat/v1/data/pivot").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).pivot(
            ids="1",
            metrics="ym:s:visits",
            dimensions="ym:s:operatingSystem",
            pivot_dimensions="ym:s:browser",
            pivot_limit=50,
            pivot_offset=10,
        )
    params = respx.calls[-1].request.url.params
    assert params["pivot_limit"] == "50"
    assert params["pivot_offset"] == "10"


@respx.mock
def test_drilldown_only_expandable_undefined() -> None:
    respx.get(f"{BASE}/stat/v1/data/drilldown").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).drilldown(
            ids="1",
            metrics="ym:s:visits",
            dimensions="ym:s:region",
            only_expandable_undefined=True,
        )
    assert respx.calls[-1].request.url.params["only_expandable_undefined"] == "true"


@respx.mock
def test_comparison_drilldown_only_expandable_undefined() -> None:
    respx.get(f"{BASE}/stat/v1/data/comparison/drilldown").respond(
        json={"total_rows": 0}
    )
    with make_client() as c:
        Stat(c).comparison_drilldown(
            ids="1",
            metrics="ym:s:visits",
            only_expandable_undefined=True,
        )
    assert respx.calls[-1].request.url.params["only_expandable_undefined"] == "true"


@respx.mock
def test_cli_table_common_flags() -> None:
    route = respx.get(f"{BASE}/stat/v1/data").respond(json={"total_rows": 0})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "stat",
            "table",
            "--ids",
            "44147844",
            "--metrics",
            "ym:s:visits",
            "--accuracy",
            "high",
            "--proposed-accuracy",
            "--include-undefined",
            "--timezone",
            "+03:00",
            "--direct-client-logins",
            "login1,login2",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    params = route.calls.last.request.url.params
    assert params["accuracy"] == "high"
    assert params["proposed_accuracy"] == "true"
    assert params["include_undefined"] == "true"
    assert params["timezone"] == "+03:00"
    assert params["direct_client_logins"] == "login1,login2"


@respx.mock
def test_cli_bytime_annotation_params() -> None:
    route = respx.get(f"{BASE}/stat/v1/data/bytime").respond(json={"total_rows": 0})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "stat",
            "bytime",
            "--ids",
            "44147844",
            "--metrics",
            "ym:s:visits",
            "--top-keys",
            "10",
            "--include-annotations",
            "--annotation-groups",
            "all",
            "--keys-sort",
            "-ym:s:visits",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    params = route.calls.last.request.url.params
    assert params["top_keys"] == "10"
    assert params["include_annotations"] == "true"
    assert params["annotation_groups"] == "all"
    assert params["keys_sort"] == "-ym:s:visits"


@respx.mock
def test_cli_pivot_pivot_params() -> None:
    route = respx.get(f"{BASE}/stat/v1/data/pivot").respond(json={"total_rows": 0})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "stat",
            "pivot",
            "--ids",
            "44147844",
            "--metrics",
            "ym:s:visits",
            "--dimensions",
            "ym:s:operatingSystem",
            "--pivot-dimensions",
            "ym:s:browser",
            "--pivot-limit",
            "50",
            "--pivot-offset",
            "10",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    params = route.calls.last.request.url.params
    assert params["pivot_limit"] == "50"
    assert params["pivot_offset"] == "10"


@respx.mock
def test_cli_drilldown_only_expandable_flag() -> None:
    route = respx.get(f"{BASE}/stat/v1/data/drilldown").respond(json={"total_rows": 0})
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "stat",
            "drilldown",
            "--ids",
            "44147844",
            "--metrics",
            "ym:s:visits",
            "--dimensions",
            "ym:s:region",
            "--only-expandable-undefined",
        ],
    )
    assert result.exit_code == 0
    assert route.called
    assert route.calls.last.request.url.params["only_expandable_undefined"] == "true"
