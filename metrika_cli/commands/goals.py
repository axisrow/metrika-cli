"""Команды группы ``goals`` (Management API, resource verb)."""

from __future__ import annotations

import typer

from ..api.goals import Goals
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Цели счётчика (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело цели: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Goals:
    return Goals(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    use_deleted: bool = typer.Option(
        False, "--use-deleted", help="Включать удалённые цели."
    ),
) -> None:
    """Список целей счётчика."""
    render(
        ctx,
        _api(ctx).list(
            counter_id, use_deleted=use_deleted, pretty=get_state(ctx).pretty
        ),
    )


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    goal_id: int = typer.Argument(..., help="ID цели."),
) -> None:
    """Информация о цели."""
    render(ctx, _api(ctx).get(counter_id, goal_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать цель (тело: {"goal": {...}})."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    goal_id: int = typer.Argument(..., help="ID цели."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Изменить цель (тело: {"goal": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id, goal_id, parse_data(data), pretty=get_state(ctx).pretty
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    goal_id: int = typer.Argument(..., help="ID цели."),
) -> None:
    """Удалить цель."""
    render(ctx, _api(ctx).delete(counter_id, goal_id, pretty=get_state(ctx).pretty))


@app.command("messengers")
@handle_errors
def messengers(ctx: typer.Context) -> None:
    """Справочник мессенджеров (для целей-чатов)."""
    render(ctx, _api(ctx).messengers(pretty=get_state(ctx).pretty))


@app.command("social-networks")
@handle_errors
def social_networks(ctx: typer.Context) -> None:
    """Справочник социальных сетей (для целей-соцсетей)."""
    render(ctx, _api(ctx).social_networks(pretty=get_state(ctx).pretty))
