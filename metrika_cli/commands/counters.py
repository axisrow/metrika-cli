"""Команды группы ``counters`` (Management API, resource verb)."""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from ..api.counters import Counters
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Счётчики (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело счётчика: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Counters:
    return Counters(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    per_page: Annotated[
        Optional[int],
        typer.Option(
            "--per-page", help="Счётчиков на страницу (≤10000, дефолт API 1000)."
        ),
    ] = None,
    offset: Annotated[
        Optional[int],
        typer.Option("--offset", help="Порядковый номер первого счётчика (с 1)."),
    ] = None,
    all_pages: Annotated[
        bool,
        typer.Option("--all", help="Забрать все страницы (цикл по offset до rows)."),
    ] = False,
) -> None:
    """Список доступных счётчиков."""
    render(
        ctx,
        _api(ctx).list(
            per_page=per_page,
            offset=offset,
            all_pages=all_pages,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Информация о счётчике."""
    render(ctx, _api(ctx).get(counter_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать счётчик (тело: {"counter": {...}})."""
    render(ctx, _api(ctx).create(parse_data(data), pretty=get_state(ctx).pretty))


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить счётчик (тело: {"counter": {...}})."""
    render(
        ctx,
        _api(ctx).edit(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Удалить счётчик."""
    render(ctx, _api(ctx).delete(counter_id, pretty=get_state(ctx).pretty))
