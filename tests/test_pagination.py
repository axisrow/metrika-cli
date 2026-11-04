"""Пагинация list-эндпоинтов (issue 13).

По официальным докам (openapi-справочник, ревизия r21770580):
- ``GET management/v1/counters`` — есть ``per_page`` (≤10000, default 1000)
  и ``offset`` (с 1), ответ содержит ``rows`` — общее число счётчиков.
- ``GET management/v1/counter/{id}/logrequests`` — пагинации НЕТ: единственный
  параметр path-``counterId``, ответ ``{"requests": [...]}`` без счётчика.
"""

import httpx
import pytest
import respx

from metrika_cli.api.counters import Counters
from metrika_cli.api.logs import Logs
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_counters_list_page_params() -> None:
    respx.get(f"{BASE}/management/v1/counters").respond(
        json={"rows": 0, "counters": []}
    )
    with make_client() as c:
        Counters(c).list(per_page=100, offset=201)
    req = respx.calls[-1].request
    assert req.url.params["per_page"] == "100"
    assert req.url.params["offset"] == "201"


@respx.mock
def test_counters_list_no_page_params_by_default() -> None:
    respx.get(f"{BASE}/management/v1/counters").respond(
        json={"rows": 0, "counters": []}
    )
    with make_client() as c:
        Counters(c).list()
    # без опций отправляется только offset=1 (равен API-дефолту), per_page — нет
    assert dict(respx.calls[-1].request.url.params) == {"offset": "1"}


@respx.mock
def test_counters_list_all_pages() -> None:
    route = respx.get(f"{BASE}/management/v1/counters").mock(
        side_effect=[
            httpx.Response(200, json={"rows": 4, "counters": [{"id": 1}, {"id": 2}]}),
            httpx.Response(200, json={"rows": 4, "counters": [{"id": 3}, {"id": 4}]}),
        ]
    )
    with make_client() as c:
        data = Counters(c).list(per_page=2, all_pages=True)
    assert [x["id"] for x in data["counters"]] == [1, 2, 3, 4]
    assert len(route.calls) == 2
    assert route.calls[1].request.url.params["offset"] == "3"
    assert route.calls[1].request.url.params["per_page"] == "2"


@respx.mock
def test_counters_list_all_pages_stops_on_empty_page() -> None:
    """rows меньше собранного (гонка с удалением) — пустая страница не циклит."""
    route = respx.get(f"{BASE}/management/v1/counters").mock(
        side_effect=[
            httpx.Response(200, json={"rows": 5, "counters": [{"id": 1}]}),
            httpx.Response(200, json={"rows": 5, "counters": []}),
        ]
    )
    with make_client() as c:
        data = Counters(c).list(all_pages=True)
    assert [x["id"] for x in data["counters"]] == [1]
    assert len(route.calls) == 2


@respx.mock
def test_counters_list_all_pages_stops_without_rows() -> None:
    """Нет rows в ответе — только одна страница (пагинация недоказуема)."""
    route = respx.get(f"{BASE}/management/v1/counters").respond(
        json={"counters": [{"id": 1}]}
    )
    with make_client() as c:
        data = Counters(c).list(all_pages=True)
    assert [x["id"] for x in data["counters"]] == [1]
    assert len(route.calls) == 1


@respx.mock
def test_logrequests_list_has_no_pagination() -> None:
    """Контракт getLogRequests: query-параметров нет (контракт без пагинации)."""
    respx.get(f"{BASE}/management/v1/counter/1/logrequests").respond(
        json={"requests": []}
    )
    with make_client() as c:
        Logs(c).list(1)
    assert dict(respx.calls[-1].request.url.params) == {}
