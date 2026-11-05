"""Команды группы ``export`` (экспорт данных в Yandex Cloud, /export/v1)."""

from __future__ import annotations

import typer

from ..api.export import CloudExport
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(
    help="Экспорт в Yandex Cloud (/export/v1).", no_args_is_help=True
)


def _api(ctx: typer.Context) -> CloudExport:
    return CloudExport(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Объекты, экспортируемые в Yandex Cloud."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    ce_id: int = typer.Argument(..., help="ID экспорта в Yandex Cloud (из export list)."),
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Отключить экспорт счётчика в Yandex Cloud."""
    render(
        ctx,
        _api(ctx).delete(ce_id, counter_id, pretty=get_state(ctx).pretty),
    )
