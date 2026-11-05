"""Команды группы ``clients`` (Management API: клиенты Директа)."""

from __future__ import annotations

import typer

from ..api.clients import Clients
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Клиенты Директа (Management API).", no_args_is_help=True)


def _api(ctx: typer.Context) -> Clients:
    return Clients(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counters: str = typer.Option(
        ...,
        "--counters",
        help="ID счётчиков через запятую (обязательный query-параметр API).",
    ),
) -> None:
    """Список клиентов Яндекс Директа по счётчикам."""
    render(ctx, _api(ctx).list(counters, pretty=get_state(ctx).pretty))
