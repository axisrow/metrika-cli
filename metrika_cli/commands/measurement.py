"""Команды группы ``measurement`` (Measurement Protocol, Management API)."""

from __future__ import annotations

import typer

from ..api.measurement import Measurement
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(
    help="Measurement Protocol: токены счётчика (Management API).",
    no_args_is_help=True,
)


def _api(ctx: typer.Context) -> Measurement:
    return Measurement(get_state(ctx).client())


@app.command("generate")
@handle_errors
def generate(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Сгенерировать токен Measurement Protocol."""
    render(ctx, _api(ctx).generate(counter_id, pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    token: str = typer.Option(
        ...,
        "--token",
        help="Токен для удаления (обязательный query-параметр API).",
    ),
) -> None:
    """Удалить токен Measurement Protocol."""
    render(
        ctx,
        _api(ctx).delete(counter_id, token, pretty=get_state(ctx).pretty),
    )
