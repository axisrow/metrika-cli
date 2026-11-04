"""Команды группы ``annotations`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.annotations import Annotations
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(
    help="Графические аннотации счётчика (Management API).", no_args_is_help=True
)

DATA_HELP = "JSON-тело примечания: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Annotations:
    return Annotations(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Список примечаний на графиках счётчика."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    annotation_id: int = typer.Argument(..., help="ID примечания."),
) -> None:
    """Информация о примечании на графике."""
    render(
        ctx,
        _api(ctx).get(counter_id, annotation_id, pretty=get_state(ctx).pretty),
    )


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать примечание (тело: {"chart_annotation": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    annotation_id: int = typer.Argument(..., help="ID примечания."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить примечание (тело: {"chart_annotation": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id, annotation_id, parse_data(data), pretty=get_state(ctx).pretty
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    annotation_id: int = typer.Argument(..., help="ID примечания."),
) -> None:
    """Удалить примечание."""
    render(
        ctx,
        _api(ctx).delete(counter_id, annotation_id, pretty=get_state(ctx).pretty),
    )
