"""Команды группы ``accounts`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.accounts import Accounts
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Аккаунты пользователя (Management API).", no_args_is_help=True)

DATA_HELP = "JSON: список аккаунтов [...], строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Accounts:
    return Accounts(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(ctx: typer.Context) -> None:
    """Список аккаунтов пользователя."""
    render(ctx, _api(ctx).list(pretty=get_state(ctx).pretty))


@app.command("update")
@handle_errors
def update(
    ctx: typer.Context,
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Заменить список аккаунтов (тело: {"accounts": [...]})."""
    render(ctx, _api(ctx).update(parse_data(data), pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    user_login: str = typer.Argument(..., help="Логин пользователя Яндекса."),
) -> None:
    """Удалить аккаунт (логин — query-параметром, по openapi)."""
    render(ctx, _api(ctx).delete(user_login, pretty=get_state(ctx).pretty))
