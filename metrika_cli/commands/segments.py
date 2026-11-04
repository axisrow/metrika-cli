"""Команды группы ``segments`` (Management API, apisegment)."""

from __future__ import annotations


import typer

from ..api.segments import Segments
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Сегменты счётчика (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело сегмента: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Segments:
    return Segments(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Список сегментов счётчика."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    segment_id: str = typer.Argument(..., help="ID сегмента."),
) -> None:
    """Информация о сегменте."""
    render(ctx, _api(ctx).get(counter_id, segment_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать сегмент (тело: {"segment": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    segment_id: str = typer.Argument(..., help="ID сегмента."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить сегмент (тело: {"segment": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id, segment_id, parse_data(data), pretty=get_state(ctx).pretty
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    segment_id: str = typer.Argument(..., help="ID сегмента."),
) -> None:
    """Удалить сегмент."""
    render(ctx, _api(ctx).delete(counter_id, segment_id, pretty=get_state(ctx).pretty))
