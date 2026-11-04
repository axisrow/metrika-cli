"""Интеграционные проверки группы operations: api-ресурс строит правильный запрос."""

import json

import pytest
import respx

from metrika_cli.api.operations import Operations
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_operations_list_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/operations").respond(
        json={"operations": []}
    )
    with make_client() as c:
        Operations(c).list(123)
    assert route.called


@respx.mock
def test_operation_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/operation/7").respond(
        json={"operation": {}}
    )
    with make_client() as c:
        Operations(c).get(123, 7)
    assert route.called


@respx.mock
def test_operations_create_wraps_body() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/operations").respond(
        json={"operation": {}}
    )
    with make_client() as c:
        Operations(c).create(123, {"action": "delete", "attr": "goal_id"})
    assert route.called
    req = respx.calls[-1].request
    assert json.loads(req.content) == {
        "operation": {"action": "delete", "attr": "goal_id"}
    }


@respx.mock
def test_operation_edit_method_and_body() -> None:
    route = respx.put(f"{BASE}/management/v1/counter/123/operation/7").respond(
        json={"operation": {}}
    )
    with make_client() as c:
        Operations(c).edit(123, 7, {"action": "delete"})
    assert route.called
    req = respx.calls[-1].request
    assert req.method == "PUT"
    assert json.loads(req.content) == {"operation": {"action": "delete"}}


@respx.mock
def test_operation_delete_method() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/operation/7").respond(
        json={"success": True}
    )
    with make_client() as c:
        Operations(c).delete(123, 7)
    assert route.called
    assert respx.calls[-1].request.method == "DELETE"
