"""Команды группы ``user_params`` (параметры посетителей, Data Import).

Формат CSV и openapi-описание — страницы user_params Management API:
https://yandex.ru/dev/metrika/ru/management/openapi/user_params/
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ..api.user_params import UserParams
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Параметры посетителей (Data Import).", no_args_is_help=True)

ACTION_HELP = "Действие: update — добавить (default) | delete_keys — удалить."
DATA_HELP = 'JSON-тело: объект загрузки {"id":…, "status":…} (строка, @файл или -).'


def _api(ctx: typer.Context) -> UserParams:
    return UserParams(get_state(ctx).client())


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
        ..., "--file", help="Путь к CSV-файлу с параметрами (multipart)."
    ),
    action: str = typer.Option("update", help=ACTION_HELP),
) -> None:
    """Загрузить параметры посетителей из CSV (multipart-запрос)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload(counter_id, file, action=action, pretty=get_state(ctx).pretty),
    )


@app.command("uploadings")
@handle_errors
def uploadings(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    limit: Optional[int] = typer.Option(None, help="Количество (default 10000)."),
    offset: Optional[int] = typer.Option(None, help="Смещение (default 0)."),
) -> None:
    """Список загрузок параметров счётчика."""
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
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    uploading_id: int = typer.Argument(..., help="ID загрузки."),
) -> None:
    """Информация о загрузке параметров по ID."""
    render(
        ctx,
        _api(ctx).uploading(counter_id, uploading_id, pretty=get_state(ctx).pretty),
    )


@app.command("confirm")
@handle_errors
def confirm(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    uploading_id: int = typer.Argument(..., help="ID загрузки."),
    data: Optional[str] = typer.Option(None, "--data", help=DATA_HELP),
) -> None:
    """Подтвердить загрузку параметров."""
    uploading = parse_data(data) if data is not None else None
    render(
        ctx,
        _api(ctx).confirm(
            counter_id,
            uploading_id,
            uploading=uploading,
            pretty=get_state(ctx).pretty,
        ),
    )
