"""Юнит-проверки транспорта: заголовки, JSON, ошибки, ретрай 429, raw."""

import httpx
import pytest
import respx

from metrika_cli.client import APIError, Client
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
    monkeypatch.setattr("metrika_cli.client._sleep", lambda s: None)
    respx.get(f"{BASE}/x").mock(
        side_effect=[
            httpx.Response(429, headers={"Retry-After": "0"}),
            httpx.Response(200, json={"ok": 1}),
        ]
    )
    with make_client() as c:
        assert c.request("GET", "x") == {"ok": 1}


@respx.mock
def test_raw_text() -> None:
    respx.get(f"{BASE}/stat/v1/data.csv").respond(
        content=b"a,b\n1,2", headers={"Content-Type": "text/csv"}
    )
    with make_client() as c:
        assert c.request("GET", "stat/v1/data.csv", raw=True) == "a,b\n1,2"
