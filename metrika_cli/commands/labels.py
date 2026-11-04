"""Команды группы ``labels`` (Management API, resource verb)."""

from __future__ import annotations


import typer

from ..api.labels import Labels
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(
    help="Метки и привязка к счётчикам (Management API).", no_args_is_help=True
)

DATA_HELP = "JSON-тело метки: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Labels:
    return Labels(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(ctx: typer.Context) -> None:
    """Список меток пользователя."""
    render(ctx, _api(ctx).list(pretty=get_state(ctx).pretty))


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    label_id: int = typer.Argument(..., help="ID метки."),
) -> None:
    """Информация о метке."""
    render(ctx, _api(ctx).get(label_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать метку (тело: {"label": {...}})."""
    render(ctx, _api(ctx).create(parse_data(data), pretty=get_state(ctx).pretty))


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    label_id: int = typer.Argument(..., help="ID метки."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить метку (тело: {"label": {...}})."""
    render(
        ctx,
        _api(ctx).edit(label_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    label_id: int = typer.Argument(..., help="ID метки."),
) -> None:
    """Удалить метку."""
    render(ctx, _api(ctx).delete(label_id, pretty=get_state(ctx).pretty))


@app.command("link")
@handle_errors
def link(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    label_id: int = typer.Argument(..., help="ID метки."),
) -> None:
    """Привязать счётчик к метке."""
    render(
        ctx,
        _api(ctx).link(counter_id, label_id, pretty=get_state(ctx).pretty),
    )


@app.command("unlink")
@handle_errors
def unlink(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    label_id: int = typer.Argument(..., help="ID метки."),
) -> None:
    """Отвязать счётчик от метки."""
    render(
        ctx,
        _api(ctx).unlink(counter_id, label_id, pretty=get_state(ctx).pretty),
    )
