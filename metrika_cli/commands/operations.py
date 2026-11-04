"""Команды группы ``operations`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.operations import Operations
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Операции счётчика (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело операции: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Operations:
    return Operations(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Список операций счётчика."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    operation_id: int = typer.Argument(..., help="ID операции."),
) -> None:
    """Информация об операции."""
    render(
        ctx,
        _api(ctx).get(counter_id, operation_id, pretty=get_state(ctx).pretty),
    )


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать операцию (тело: {"operation": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    operation_id: int = typer.Argument(..., help="ID операции."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить операцию (тело: {"operation": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id,
            operation_id,
            parse_data(data),
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    operation_id: int = typer.Argument(..., help="ID операции."),
) -> None:
    """Удалить операцию."""
    render(
        ctx,
        _api(ctx).delete(counter_id, operation_id, pretty=get_state(ctx).pretty),
    )
