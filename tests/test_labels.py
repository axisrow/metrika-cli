"""Интеграционные проверки группы labels: пути и тела запросов."""

import json

import pytest
import respx

from metrika_cli.api.labels import Labels
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_labels_list() -> None:
    route = respx.get(f"{BASE}/management/v1/labels").respond(json={"labels": []})
    with make_client() as c:
        Labels(c).list()
    assert route.called


@respx.mock
def test_label_create_body() -> None:
    route = respx.post(f"{BASE}/management/v1/labels").respond(json={"label": {}})
    with make_client() as c:
        Labels(c).create({"name": "promo"})
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"label": {"name": "promo"}}


@respx.mock
def test_label_get_path() -> None:
    route = respx.get(f"{BASE}/management/v1/label/77").respond(json={"label": {}})
    with make_client() as c:
        Labels(c).get(77)
    assert route.called


@respx.mock
def test_label_edit_body() -> None:
    route = respx.put(f"{BASE}/management/v1/label/77").respond(json={"label": {}})
    with make_client() as c:
        Labels(c).edit(77, {"name": "new"})
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"label": {"name": "new"}}


@respx.mock
def test_label_delete_method() -> None:
    route = respx.delete(f"{BASE}/management/v1/label/77").respond(json={})
    with make_client() as c:
        Labels(c).delete(77)
    assert route.called


@respx.mock
def test_link_path_and_method() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/label/77").respond(json={})
    with make_client() as c:
        Labels(c).link(123, 77)
    assert route.called


@respx.mock
def test_unlink_path_and_method() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/label/77").respond(json={})
    with make_client() as c:
        Labels(c).unlink(123, 77)
    assert route.called
