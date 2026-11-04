"""Команды группы ``delegates`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.delegates import Delegates
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Представители (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело представителя: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Delegates:
    return Delegates(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(ctx: typer.Context) -> None:
    """Список представителей."""
    render(ctx, _api(ctx).list(pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Добавить представителя (тело: {"delegate": {...}})."""
    render(ctx, _api(ctx).create(parse_data(data), pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    user_login: str = typer.Argument(..., help="Логин пользователя Яндекса."),
) -> None:
    """Удалить представителя (логин — query-параметром, по openapi)."""
    render(ctx, _api(ctx).delete(user_login, pretty=get_state(ctx).pretty))
