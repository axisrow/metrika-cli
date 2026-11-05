"""Интеграционные проверки группы grants: api-слой и CLI строят правильные запросы.

Пути и методы сверены с официальным openapi
(https://yandex.ru/dev/metrika/ru/management/openapi/grant/*.md).
"""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.grants import Grants
from metrika_cli.cli import app
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

BASE = "https://api-metrika.yandex.net"

runner = CliRunner()


def make_client() -> Client:
    return Client(Config(token="T"))


@respx.mock
def test_grants_list() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/grants").respond(
        json={"grants": []}
    )
    with make_client() as c:
        Grants(c).list(123)
    assert route.called


@respx.mock
def test_grants_create_wraps_grant() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/grants").respond(json={})
    with make_client() as c:
        Grants(c).create(123, {"user_login": "alice", "perm": "view"})
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"grant": {"user_login": "alice", "perm": "view"}}


@respx.mock
def test_grants_delete_user_login_is_query_param() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/grant").respond(
        json={"success": True}
    )
    with make_client() as c:
        Grants(c).delete(123, "alice")
    assert route.called
    assert respx.calls[-1].request.url.params["user_login"] == "alice"


@respx.mock
def test_grants_delete_user_uid_alternative() -> None:
    """user_uid — альтернатива user_login (openapi deleteGrant.md)."""
    respx.delete(f"{BASE}/management/v1/counter/123/grant").respond(
        json={"success": True}
    )
    with make_client() as c:
        Grants(c).delete(123, user_uid=42)
    params = respx.calls[-1].request.url.params
    assert params["user_uid"] == "42"
    assert "user_login" not in params


@respx.mock
def test_grants_get_user_login_required_query_param() -> None:
    """GET grant: user_login — обязательный query-параметр (openapi grant.md)."""
    respx.get(f"{BASE}/management/v1/counter/123/grant").respond(json={})
    with make_client() as c:
        Grants(c).get(123, "alice")
    assert respx.calls[-1].request.url.params["user_login"] == "alice"


@respx.mock
def test_grants_edit_wraps_grant() -> None:
    """PUT grant: тело {"grant": {...}} (openapi editGrant.md)."""
    respx.put(f"{BASE}/management/v1/counter/123/grant").respond(json={})
    with make_client() as c:
        Grants(c).edit(123, {"user_login": "alice", "perm": "edit"})
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"grant": {"user_login": "alice", "perm": "edit"}}


@respx.mock
def test_grants_my_grant() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/my_grant").respond(json={})
    with make_client() as c:
        Grants(c).my_grant(123)
    assert route.called
    assert not respx.calls[-1].request.url.params


@respx.mock
def test_grants_public_set_posts_without_body() -> None:
    route = respx.post(f"{BASE}/management/v1/counter/123/public_grant").respond(
        json={"perm": "public_stat"}
    )
    with make_client() as c:
        Grants(c).public_set(123)
    assert route.called
    assert respx.calls[-1].request.read() == b""


@respx.mock
def test_grants_public_delete() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/public_grant").respond(
        json={"success": True}
    )
    with make_client() as c:
        Grants(c).public_delete(123)
    assert route.called


@respx.mock
def test_cli_create_default_perm_is_view() -> None:
    """Консервативный дефолт: без --perm выдаётся минимальный доступ view."""
    route = respx.post(f"{BASE}/management/v1/counter/123/grants").respond(json={})
    result = runner.invoke(
        app, ["--token", "T", "grants", "create", "123", "--user-login", "alice"]
    )
    assert result.exit_code == 0
    assert route.called
    body = json.loads(respx.calls[-1].request.read())
    assert body == {"grant": {"user_login": "alice", "perm": "view"}}


@respx.mock
def test_cli_delete_passes_user_login() -> None:
    route = respx.delete(f"{BASE}/management/v1/counter/123/grant").respond(
        json={"success": True}
    )
    result = runner.invoke(
        app, ["--token", "T", "grants", "delete", "123", "--user-login", "alice"]
    )
    assert result.exit_code == 0
    assert route.called
    assert respx.calls[-1].request.url.params["user_login"] == "alice"


@respx.mock
def test_cli_delete_user_uid() -> None:
    respx.delete(f"{BASE}/management/v1/counter/123/grant").respond(
        json={"success": True}
    )
    result = runner.invoke(app, ["--token", "T", "grants", "delete", "123", "--user-uid", "42"])
    assert result.exit_code == 0
    params = respx.calls[-1].request.url.params
    assert params["user_uid"] == "42"
    assert "user_login" not in params


def test_cli_delete_requires_login_or_uid() -> None:
    """Без идентификатора пользователя — ошибка использования, без запроса."""
    result = runner.invoke(app, ["--token", "T", "grants", "delete", "123"])
    assert result.exit_code != 0
    assert "--user-login" in result.output


@respx.mock
def test_cli_get_user_login() -> None:
    respx.get(f"{BASE}/management/v1/counter/123/grant").respond(
        json={"perm": "view"}
    )
    result = runner.invoke(
        app, ["--token", "T", "grants", "get", "123", "--user-login", "alice"]
    )
    assert result.exit_code == 0
    assert respx.calls[-1].request.url.params["user_login"] == "alice"


@respx.mock
def test_cli_edit_wraps_grant() -> None:
    respx.put(f"{BASE}/management/v1/counter/123/grant").respond(json={})
    result = runner.invoke(
        app,
        [
            "--token",
            "T",
            "grants",
            "edit",
            "123",
            "--user-login",
            "alice",
            "--perm",
            "edit",
            "--comment",
            "обновлено",
        ],
    )
    assert result.exit_code == 0
    body = json.loads(respx.calls[-1].request.read())
    assert body == {
        "grant": {
            "user_login": "alice",
            "perm": "edit",
            "comment": "обновлено",
        }
    }


@respx.mock
def test_cli_my_grant() -> None:
    route = respx.get(f"{BASE}/management/v1/counter/123/my_grant").respond(json={})
    result = runner.invoke(app, ["--token", "T", "grants", "my-grant", "123"])
    assert result.exit_code == 0
    assert route.called


@respx.mock
def test_cli_public_set_and_delete() -> None:
    post_route = respx.post(f"{BASE}/management/v1/counter/123/public_grant").respond(
        json={"perm": "public_stat"}
    )
    del_route = respx.delete(f"{BASE}/management/v1/counter/123/public_grant").respond(
        json={"success": True}
    )
    result = runner.invoke(app, ["--token", "T", "grants", "public-set", "123"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["--token", "T", "grants", "public-delete", "123"])
    assert result.exit_code == 0
    assert post_route.called
    assert del_route.called
