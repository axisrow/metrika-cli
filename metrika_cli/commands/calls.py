"""Команды группы ``calls`` (офлайн-звонки, Data Import).

Формат CSV — гайд «Передача данных о звонках»:
https://yandex.ru/dev/metrika/ru/management/calls.md
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ..api.calls import Calls
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Офлайн-звонки (Data Import).", no_args_is_help=True)

CLIENT_ID_TYPE_HELP = "Тип ID в колонках CSV: USER_ID | CLIENT_ID | YCLID."


def _api(ctx: typer.Context) -> Calls:
    return Calls(get_state(ctx).client())


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
        ..., "--file", help="Путь к CSV-файлу со звонками (multipart)."
    ),
    client_id_type: str = typer.Option(
        ..., "--client-id-type", help=CLIENT_ID_TYPE_HELP
    ),
    comment: Optional[str] = typer.Option(
        None, help="Комментарий к загрузке (≤255 символов)."
    ),
    new_goal_name: Optional[str] = typer.Option(
        None, help="Имя цели «звонки», создаваемой автоматически."
    ),
) -> None:
    """Загрузить офлайн-звонки из CSV (multipart-запрос)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload(
            counter_id,
            file,
            client_id_type=client_id_type,
            comment=comment,
            new_goal_name=new_goal_name,
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
) -> None:
    """Список загрузок звонков счётчика."""
    render(
        ctx,
        _api(ctx).uploadings(
            counter_id, limit=limit, offset=offset, pretty=get_state(ctx).pretty
        ),
    )


@app.command("uploading")
@handle_errors
def uploading(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    id: int = typer.Argument(..., help="ID загрузки."),
) -> None:
    """Информация о загрузке звонков по ID."""
    render(ctx, _api(ctx).uploading(counter_id, id, pretty=get_state(ctx).pretty))
