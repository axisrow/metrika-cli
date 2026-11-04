"""Команды группы ``logs`` (Logs API: evaluate→create→poll→download)."""

from __future__ import annotations

from typing import Optional

import typer

from ..api.logs import Logs
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render
from ..output import print_json

app = typer.Typer(help="Лог-запросы (сырые данные, Logs API).", no_args_is_help=True)

DATA_HELP = "JSON-тело запроса: строка, @файл или - (stdin); source/date1/date2/fields."


def _api(ctx: typer.Context) -> Logs:
    return Logs(get_state(ctx).client())


@app.command("evaluate")
@handle_errors
def evaluate(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    date1: Optional[str] = typer.Option(None, help="Начало периода (YYYY-MM-DD)."),
    date2: Optional[str] = typer.Option(None, help="Конец периода."),
    source: Optional[str] = typer.Option(None, help="hits | visits."),
    fields: Optional[str] = typer.Option(
        None, help="Список полей через запятую (≤3000 символов)."
    ),
) -> None:
    """Оценить, вернёт ли лог-запрос данные."""
    render(
        ctx,
        _api(ctx).evaluate(
            counter_id,
            date1=date1,
            date2=date2,
            source=source,
            fields=fields,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("list")
@handle_errors
def list_(ctx: typer.Context, counter_id: int = typer.Argument(...)) -> None:
    """Список лог-запросов счётчика."""
    render(ctx, _api(ctx).list(counter_id, pretty=get_state(ctx).pretty))


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
) -> None:
    """Создать лог-запрос (период ≤1 год; квота 10 ГБ/счётчик)."""
    render(
        ctx,
        _api(ctx).create(counter_id, parse_data(data), pretty=get_state(ctx).pretty),
    )


@app.command("info")
@handle_errors
def info(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    request_id: int = typer.Argument(...),
) -> None:
    """Статус лог-запроса (poll до processed; parts)."""
    render(ctx, _api(ctx).info(counter_id, request_id, pretty=get_state(ctx).pretty))


@app.command("cancel")
@handle_errors
def cancel(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    request_id: int = typer.Argument(...),
) -> None:
    """Отменить необработанный запрос."""
    render(ctx, _api(ctx).cancel(counter_id, request_id, pretty=get_state(ctx).pretty))


@app.command("clean")
@handle_errors
def clean(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    request_id: int = typer.Argument(...),
) -> None:
    """Удалить части обработанного запроса (освободить квоту)."""
    render(ctx, _api(ctx).clean(counter_id, request_id, pretty=get_state(ctx).pretty))


@app.command("download-part")
@handle_errors
def download_part(
    ctx: typer.Context,
    counter_id: int = typer.Argument(...),
    request_id: int = typer.Argument(...),
    part: int = typer.Option(0, "--part", help="Номер части (partNumber)."),
    out: Optional[str] = typer.Option(None, "--out", help="Записать CSV в файл."),
) -> None:
    """Скачать CSV-часть выгрузки (в файл --out или stdout)."""
    text = _api(ctx).download_part(counter_id, request_id, part)
    if out:
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print_json({"ok": True, "out": out, "bytes": len(text)})
    else:
        typer.echo(text)
