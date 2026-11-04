"""Команды группы ``filters`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.filters import Filters
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Фильтры счётчика (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело фильтра: строка, @файл или - (stdin)."

COUNTER_HELP = "ID счётчика."
FILTER_HELP = "ID фильтра."


def _api(ctx: typer.Context) -> Filters:
    return Filters(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help=COUNTER_HELP),
) -> None:
    """Список фильтров счётчика (не более 30 на счётчик)."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help=COUNTER_HELP),
    filter_id: int = typer.Argument(..., help=FILTER_HELP),
) -> None:
    """Информация о фильтре."""
    render(ctx, _api(ctx).get(counter_id, filter_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help=COUNTER_HELP),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать фильтр (тело: {"filter": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help=COUNTER_HELP),
    filter_id: int = typer.Argument(..., help=FILTER_HELP),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить фильтр (тело: {"filter": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id, filter_id, parse_data(data), pretty=get_state(ctx).pretty
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help=COUNTER_HELP),
    filter_id: int = typer.Argument(..., help=FILTER_HELP),
) -> None:
    """Удалить фильтр."""
    render(ctx, _api(ctx).delete(counter_id, filter_id, pretty=get_state(ctx).pretty))
