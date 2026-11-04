"""Юнит-проверки транспорта: заголовки, JSON, ошибки, ретрай 429, raw."""

import httpx
import pytest
import respx

from metrika_cli.client import APIError, Client, RateLimitError
from metrika_cli.config import Config

pytestmark = pytest.mark.unit

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_success_json() -> None:
    respx.get(f"{BASE}/management/v1/counters").respond(json={"counters": []})
    with make_client() as c:
        assert c.request("GET", "management/v1/counters") == {"counters": []}


@respx.mock
def test_oauth_header() -> None:
    route = respx.get(f"{BASE}/management/v1/counters").respond(json={})
    with make_client() as c:
        c.request("GET", "management/v1/counters")
    assert route.calls.last.request.headers["Authorization"] == "OAuth T"


@respx.mock
def test_error_envelope() -> None:
    respx.get(f"{BASE}/x").respond(
        status_code=400,
        json={"errors": [{"error_type": "bad", "message": "нет цели"}]},
    )
    with make_client() as c, pytest.raises(APIError) as exc:
        c.request("GET", "x")
    assert "нет цели" in str(exc.value)
    assert exc.value.status_code == 400


@respx.mock
def test_429_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Экспоненциальный backoff: два 429, паузы 30с → 60с, потом успех."""
    waits: list[float] = []
    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: waits.append(s))
    respx.get(f"{BASE}/x").mock(
        side_effect=[
            httpx.Response(429),
            httpx.Response(429),
            httpx.Response(200, json={"ok": 1}),
        ]
    )
    with make_client() as c:
        assert c.request("GET", "x") == {"ok": 1}
    assert waits == [30.0, 60.0]


@respx.mock
def test_429_retry_after_header(monkeypatch: pytest.MonkeyPatch) -> None:
    """Retry-After от API перекрывает экспоненциальный backoff."""
    waits: list[float] = []
    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: waits.append(s))
    respx.get(f"{BASE}/x").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "7"}),
            httpx.Response(200, json={"ok": 1}),
        ]
    )
    with make_client() as c:
        assert c.request("GET", "x") == {"ok": 1}
    assert waits == [7.0]


@respx.mock
def test_429_exhausted(monkeypatch: pytest.MonkeyPatch) -> None:
    """Исчерпание ретраев: 429 на все 3 попытки — RateLimitError.

    side_effect даёт ровно 3 ответа: четвёртый запрос упал бы моком,
    поэтому тест попутно фиксирует количество запросов.
    """
    waits: list[float] = []
    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: waits.append(s))
    respx.get(f"{BASE}/x").mock(
        side_effect=[
            httpx.Response(429),
            httpx.Response(429),
            httpx.Response(429),
        ]
    )
    with make_client() as c, pytest.raises(RateLimitError):
        c.request("GET", "x")
    assert waits == [30.0, 60.0]


@respx.mock
def test_raw_text() -> None:
    respx.get(f"{BASE}/stat/v1/data.csv").respond(
        content=b"a,b\n1,2", headers={"Content-Type": "text/csv"}
    )
    with make_client() as c:
        assert c.request("GET", "stat/v1/data.csv", raw=True) == "a,b\n1,2"
