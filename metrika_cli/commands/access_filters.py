"""Команды группы ``access_filters`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.access_filters import AccessFilters
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Фильтры доступа (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело фильтра доступа: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> AccessFilters:
    return AccessFilters(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Список фильтров доступа счётчика."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    access_filter_id: int = typer.Argument(..., help="ID фильтра доступа."),
) -> None:
    """Информация о фильтре доступа."""
    render(
        ctx,
        _api(ctx).get(counter_id, access_filter_id, pretty=get_state(ctx).pretty),
    )


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать фильтр доступа (тело: {"access_filter": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    access_filter_id: int = typer.Argument(..., help="ID фильтра доступа."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить фильтр доступа (тело: {"access_filter": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id,
            access_filter_id,
            parse_data(data),
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    access_filter_id: int = typer.Argument(..., help="ID фильтра доступа."),
    delete_grants: bool = typer.Option(
        False,
        "--delete-grants / --keep-grants",
        help="Также удалить гранты, выданные на этот фильтр (по умолчанию нет).",
    ),
) -> None:
    """Удалить фильтр доступа."""
    render(
        ctx,
        _api(ctx).delete(
            counter_id,
            access_filter_id,
            delete_grants=delete_grants,
            pretty=get_state(ctx).pretty,
        ),
    )
