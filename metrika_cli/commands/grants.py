"""Команды группы ``grants`` (Management API, resource verb)."""

from __future__ import annotations

from enum import Enum
from typing import Optional

import typer

from ..api.grants import Grants
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Доступы к счётчику (Management API).", no_args_is_help=True)


class Perm(str, Enum):
    """Уровни доступа (openapi: management/openapi/grant/addGrant.md)."""

    PUBLIC_STAT = "public_stat"
    VIEW = "view"
    EDIT = "edit"
    ANALYST = "analyst"
    ANALYST_ACCESS_FILTER = "analyst_access_filter"


def _api(ctx: typer.Context) -> Grants:
    return Grants(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Список доступов к счётчику."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    user_login: str = typer.Option(
        ..., "--user-login", help="Логин пользователя, которому выдаётся доступ."
    ),
    perm: Perm = typer.Option(
        Perm.VIEW,
        "--perm",
        help="Уровень доступа. По умолчанию view — минимальный достаточный.",
    ),
    comment: Optional[str] = typer.Option(None, "--comment", help="Комментарий."),
    partner_data_access: bool = typer.Option(
        False,
        "--partner-data-access",
        help="Дать доступ к данным партнёр-метрики (РСЯ).",
    ),
) -> None:
    """Выдать доступ пользователю (тело: {"grant": {...}}).

    Дефолты консервативные: perm=view, partner_data_access выключен.
    """
    grant: dict = {"user_login": user_login, "perm": perm.value}
    if comment:
        grant["comment"] = comment
    if partner_data_access:
        grant["partner_data_access"] = True
    render(ctx, _api(ctx).create(counter_id, grant, pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    user_login: str = typer.Option(
        ..., "--user-login", help="Логин пользователя, у которого отзывается доступ."
    ),
) -> None:
    """Отозвать доступ пользователя (user_login — query-параметр API)."""
    render(ctx, _api(ctx).delete(counter_id, user_login, pretty=get_state(ctx).pretty))


@app.command("public-set")
@handle_errors
def public_set(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Включить публичный доступ к счётчику."""
    render(ctx, _api(ctx).public_set(counter_id, pretty=get_state(ctx).pretty))


@app.command("public-delete")
@handle_errors
def public_delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Выключить публичный доступ к счётчику."""
    render(ctx, _api(ctx).public_delete(counter_id, pretty=get_state(ctx).pretty))
