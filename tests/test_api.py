"""Интеграционные проверки слоёв: api-ресурс строит правильный запрос."""

import pytest
import respx

from metrika_cli.api.counters import Counters
from metrika_cli.api.logs import Logs
from metrika_cli.api.stat import Stat
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_counters_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counters").respond(json={"counters": []})
    with make_client() as c:
        Counters(c).list()
    assert route.called


@respx.mock
def test_counter_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123").respond(json={})
    with make_client() as c:
        Counters(c).get(123)
    assert route.called


@respx.mock
def test_stat_table_params() -> None:
    respx.get(f"{BASE}/stat/v1/data").respond(json={"total_rows": 0})
    with make_client() as c:
        Stat(c).table(
            ids="44147844",
            metrics="ym:s:visits",
            dimensions="ym:s:operatingSystem",
            date1="2026-01-01",
            date2="2026-01-31",
            limit=5,
        )
    # параметры берём из последнего запроса (QueryParams отдаёт декодированные)
    req = respx.calls[-1].request
    assert req.url.params["ids"] == "44147844"
    assert req.url.params["metrics"] == "ym:s:visits"
    assert req.url.params["limit"] == "5"


@respx.mock
def test_stat_table_csv_suffix() -> None:
    route = respx.get(url=f"{BASE}/stat/v1/data.csv").respond(content=b"a,b")
    with make_client() as c:
        text = Stat(c).table(ids="1", metrics="ym:s:visits", csv=True)
    assert route.called
    assert text == "a,b"


@respx.mock
def test_log_download_part_path() -> None:
    route = respx.get(
        url=f"{BASE}/management/v1/counter/1/logrequest/2/part/0/download"
    ).respond(content=b"csv,data")
    with make_client() as c:
        text = Logs(c).download_part(1, 2, 0)
    assert route.called
    assert text == "csv,data"
