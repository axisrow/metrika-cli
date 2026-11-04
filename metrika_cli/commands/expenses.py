"""Команды группы ``expenses`` (Data Import: расходы на рекламу)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from ..api.expenses import Expenses
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Загрузка расходов (Data Import).", no_args_is_help=True)


def _api(ctx: typer.Context) -> Expenses:
    return Expenses(get_state(ctx).client())


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
        ...,
        "--file",
        help=(
            "Путь к CSV-файлу (обязательные колонки: Date, "
            "UTMSource/TrafficSource, Expenses)."
        ),
    ),
    comment: Optional[str] = typer.Option(None, help="Комментарий."),
    provider: Optional[str] = typer.Option(
        None, help="Провайдер данных (по умолчанию default)."
    ),
) -> None:
    """Загрузить расходы из CSV (multipart-запрос)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).upload(
            counter_id,
            file,
            comment=comment,
            provider=provider,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    file: str = typer.Option(
        ...,
        "--file",
        help="Путь к CSV-файлу условий удаления (обязательная колонка Date).",
    ),
    comment: Optional[str] = typer.Option(None, help="Комментарий."),
    provider: Optional[str] = typer.Option(
        None,
        help="Провайдер (без него удалятся данные всех провайдеров).",
    ),
) -> None:
    """Удалить расходы по CSV-файлу условий (multipart-запрос)."""
    _checked_path(file)
    render(
        ctx,
        _api(ctx).delete(
            counter_id,
            file,
            comment=comment,
            provider=provider,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("delete-single")
@handle_errors
def delete_single(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    date: str = typer.Option(
        ..., "--date", help="Дата: YYYY-MM-DD или диапазон YYYY-MM-DD/YYYY-MM-DD."
    ),
    traffic_source: Optional[str] = typer.Option(
        None, "--traffic-source", help="Источник трафика первого уровня."
    ),
    traffic_source_detail: Optional[str] = typer.Option(
        None, "--traffic-source-detail", help="Источник трафика второго уровня."
    ),
    utm_source: Optional[str] = typer.Option(
        None, "--utm-source", help="Метка utm_source (регистрозависимая)."
    ),
    utm_medium: Optional[str] = typer.Option(
        None, "--utm-medium", help="Метка utm_medium."
    ),
    utm_campaign: Optional[str] = typer.Option(
        None, "--utm-campaign", help="Метка utm_campaign."
    ),
    utm_term: Optional[str] = typer.Option(None, "--utm-term", help="Метка utm_term."),
    utm_content: Optional[str] = typer.Option(
        None, "--utm-content", help="Метка utm_content."
    ),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        help="Провайдер (без него удалятся данные всех провайдеров).",
    ),
    comment: Optional[str] = typer.Option(None, "--comment", help="Комментарий."),
) -> None:
    """Удалить расходы по условиям, переданным в запросе."""
    render(
        ctx,
        _api(ctx).delete_single(
            counter_id,
            date,
            traffic_source=traffic_source,
            traffic_source_detail=traffic_source_detail,
            utm_source=utm_source,
            utm_medium=utm_medium,
            utm_campaign=utm_campaign,
            utm_term=utm_term,
            utm_content=utm_content,
            provider=provider,
            comment=comment,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("uploadings")
@handle_errors
def uploadings(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    limit: Optional[int] = typer.Option(None, help="Сколько загрузок (default 10000)."),
    offset: Optional[int] = typer.Option(
        None, help="С какой загрузки начать (первая — 0)."
    ),
) -> None:
    """Список загрузок расходов."""
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
    id: int = typer.Argument(..., help="ID загрузки."),
) -> None:
    """Информация о загрузке расходов."""
    render(ctx, _api(ctx).uploading(counter_id, id, pretty=get_state(ctx).pretty))
