"""Команды группы ``conversions`` (офлайн-конверсии, Data Import).

Формат CSV — гайд «Офлайн-конверсии»:
https://yandex.ru/dev/metrika/ru/management/offline-conv.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ..api.conversions import Conversions
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Офлайн-конверсии (Data Import).", no_args_is_help=True)


def _api(ctx: typer.Context) -> Conversions:
    return Conversions(get_state(ctx).client())


def _checked_path(value: str) -> str:
    """Проверить, что путь --file существует и это файл."""
    path = Path(value)
    if not path.is_file():
        raise typer.BadParameter(f"Файл не найден: {value}")
    return value


@app.command("upload")
@handle_errors
def upload(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    file: str = typer.Option(
        ..., "--file", help="Путь к CSV-файлу с конверсиями (multipart)."
    ),
    comment: Optional[str] = typer.Option(
        None, help="Комментарий к загрузке (≤255 символов)."
    ),
    type_: Optional[str] = typer.Option(
        None, "--type", help="Тип загрузки: BASIC (default) | CALLS | CHATS."
    ),
) -> None:
    """Загрузить офлайн-конверсии из CSV (multipart-запрос)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload(
            counter_id,
            file,
            comment=comment,
            type_=type_,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("uploadings")
@handle_errors
def uploadings(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    limit: Optional[int] = typer.Option(None, help="Количество (default 10000)."),
    offset: Optional[int] = typer.Option(None, help="Смещение (default 0)."),
    type_: Optional[str] = typer.Option(
        None, "--type", help="Тип: BASIC (default) | CALLS | CHATS."
    ),
) -> None:
    """Список загрузок конверсий счётчика."""
    render(
        ctx,
        _api(ctx).uploadings(
            counter_id,
            limit=limit,
            offset=offset,
            type_=type_,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("uploading")
@handle_errors
def uploading(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    id: int = typer.Argument(..., help="ID загрузки."),
    type_: Optional[str] = typer.Option(
        None, "--type", help="Тип: BASIC (default) | CALLS | CHATS."
    ),
) -> None:
    """Информация о загрузке конверсий по ID."""
    render(
        ctx,
        _api(ctx).uploading(counter_id, id, type_=type_, pretty=get_state(ctx).pretty),
    )
