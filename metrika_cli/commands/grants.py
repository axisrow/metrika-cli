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


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    user_login: str = typer.Option(
        ...,
        "--user-login",
        help="Логин пользователя (обязательный query-параметр API).",
    ),
) -> None:
    """Информация о разрешении пользователя."""
    render(ctx, _api(ctx).get(counter_id, user_login, pretty=get_state(ctx).pretty))


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


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    user_login: str = typer.Option(
        ..., "--user-login", help="Логин пользователя, чей доступ изменяется."
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
    """Изменить разрешение пользователя (тело: {"grant": {...}})."""
    grant: dict = {"user_login": user_login, "perm": perm.value}
    if comment:
        grant["comment"] = comment
    if partner_data_access:
        grant["partner_data_access"] = True
    render(ctx, _api(ctx).edit(counter_id, grant, pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    user_login: Optional[str] = typer.Option(
        None,
        "--user-login",
        help="Логин пользователя, у которого отзывается доступ.",
    ),
    user_uid: Optional[int] = typer.Option(
        None,
        "--user-uid",
        help="UID пользователя (альтернатива --user-login).",
    ),
) -> None:
    """Отозвать доступ пользователя (user_login или user_uid — query API)."""
    if not user_login and not user_uid:
        raise typer.BadParameter("Нужен --user-login или --user-uid")
    render(
        ctx,
        _api(ctx).delete(
            counter_id, user_login, user_uid=user_uid, pretty=get_state(ctx).pretty
        ),
    )


@app.command("my-grant")
@handle_errors
def my_grant(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Разрешение текущего пользователя на счётчик."""
    render(ctx, _api(ctx).my_grant(counter_id, pretty=get_state(ctx).pretty))


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
