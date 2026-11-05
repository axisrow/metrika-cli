"""Команды группы ``cdp`` (CDP/CRM: клиенты и заказы, /cdp/api/v1)."""

from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

import typer

from ..api.cdp import Cdp
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="CDP/CRM: клиенты и заказы (/cdp/api/v1).", no_args_is_help=True)

DATA_HELP = "JSON-тело: строка, @файл или - (stdin). Объект или список."


def _api(ctx: typer.Context) -> Cdp:
    return Cdp(get_state(ctx).client())


def _checked_path(value: str) -> str:
    """Проверить, что путь --file существует и это файл."""
    path = Path(value)
    if not path.is_file():
        raise typer.BadParameter(f"Файл не найден: {value}")
    return value


class MergeMode(str, Enum):
    """Режим сохранения данных (openapi schema/uploadContacts.md)."""

    APPEND = "APPEND"
    SAVE = "SAVE"


class Delimiter(str, Enum):
    """Разделитель столбцов CSV-файла."""

    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"


def _wrap(key: str, data) -> dict:
    """Список строк обернуть в документированное тело {key: [...]}, объект
    передать как есть (полный {"key": [...]} или {"key": [...], ...})."""
    if isinstance(data, list):
        return {key: data}
    return data


@app.command("upload-contacts")
@handle_errors
def upload_contacts(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    file: str = typer.Option(..., "--file", help="Путь к CSV-файлу клиентов."),
    columns_mapping: str = typer.Option(
        ...,
        "--columns-mapping",
        help="Соответствие столбцов атрибутам (см. openapi uploadContacts).",
    ),
    merge_mode: MergeMode = typer.Option(
        ..., "--merge-mode", help="Режим сохранения: APPEND | SAVE."
    ),
    delimiter_type: Optional[Delimiter] = typer.Option(
        None, "--delimiter-type", help="Разделитель: COMMA | SEMICOLON."
    ),
) -> None:
    """Загрузить клиентов из CSV (multipart)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload_contacts(
            counter_id,
            file,
            columns_mapping=columns_mapping,
            merge_mode=merge_mode.value,
            delimiter_type=delimiter_type.value if delimiter_type else None,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("upload-contacts-json")
@handle_errors
def upload_contacts_json(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
    merge_mode: MergeMode = typer.Option(
        ..., "--merge-mode", help="Режим сохранения: APPEND | SAVE."
    ),
) -> None:
    """Загрузить клиентов из JSON (тело {"contacts": [...]})."""
    render(
        ctx,
        _api(ctx).upload_contacts_json(
            counter_id,
            _wrap("contacts", parse_data(data)),
            merge_mode=merge_mode.value,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("upload-orders")
@handle_errors
def upload_orders(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    file: str = typer.Option(..., "--file", help="Путь к CSV-файлу заказов."),
    columns_mapping: str = typer.Option(
        ...,
        "--columns-mapping",
        help="Соответствие столбцов атрибутам (см. openapi uploadOrders).",
    ),
    merge_mode: MergeMode = typer.Option(
        ..., "--merge-mode", help="Режим сохранения: APPEND | SAVE."
    ),
    delimiter_type: Optional[Delimiter] = typer.Option(
        None, "--delimiter-type", help="Разделитель: COMMA | SEMICOLON."
    ),
) -> None:
    """Загрузить заказы из CSV (multipart)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload_orders(
            counter_id,
            file,
            columns_mapping=columns_mapping,
            merge_mode=merge_mode.value,
            delimiter_type=delimiter_type.value if delimiter_type else None,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("upload-orders-json")
@handle_errors
def upload_orders_json(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
    merge_mode: MergeMode = typer.Option(
        ..., "--merge-mode", help="Режим сохранения: APPEND | SAVE."
    ),
) -> None:
    """Загрузить заказы из JSON (тело {"orders": [...]})."""
    render(
        ctx,
        _api(ctx).upload_orders_json(
            counter_id,
            _wrap("orders", parse_data(data)),
            merge_mode=merge_mode.value,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("upload-simple-orders")
@handle_errors
def upload_simple_orders(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    file: str = typer.Option(
        ..., "--file", help="Путь к CSV-файлу клиентов и заказов."
    ),
    merge_mode: MergeMode = typer.Option(
        ..., "--merge-mode", help="Режим сохранения: APPEND | SAVE."
    ),
    delimiter_type: Optional[Delimiter] = typer.Option(
        None, "--delimiter-type", help="Разделитель: COMMA | SEMICOLON."
    ),
) -> None:
    """Упрощённая загрузка клиентов и заказов из CSV (multipart)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload_simple_orders(
            counter_id,
            file,
            merge_mode=merge_mode.value,
            delimiter_type=delimiter_type.value if delimiter_type else None,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("last-uploadings")
@handle_errors
def last_uploadings(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    datetime_offset: Optional[str] = typer.Option(
        None,
        "--datetime-offset",
        help="Возвращать загрузки строго раньше (YYYY-MM-DD HH:MM:SS).",
    ),
    limit: Optional[int] = typer.Option(
        None, "--limit", help="Сколько загрузок (1..1000)."
    ),
    source: Optional[str] = typer.Option(
        None,
        "--source",
        help="Источник загрузки: API | CRM | CONVERSION_CENTER | ALBATO | UI.",
    ),
) -> None:
    """Последние загрузки CDP/CRM."""
    render(
        ctx,
        _api(ctx).last_uploadings(
            counter_id,
            datetime_offset=datetime_offset,
            limit=limit,
            source=source,
            pretty=get_state(ctx).pretty,
        ),
    )
