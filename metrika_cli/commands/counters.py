"""Команды группы ``counters`` (Management API, resource verb)."""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from ..api.counters import Counters
from ..context import get_state, handle_errors
from ..inputs import parse_data
from ..render import render

app = typer.Typer(help="Счётчики (Management API).", no_args_is_help=True)

DATA_HELP = "JSON-тело счётчика: строка, @файл или - (stdin)."


def _api(ctx: typer.Context) -> Counters:
    return Counters(get_state(ctx).client())


@app.command("list")
@handle_errors
def list_(
    ctx: typer.Context,
    per_page: Annotated[
        Optional[int],
        typer.Option(
            "--per-page", help="Счётчиков на страницу (≤10000, дефолт API 1000)."
        ),
    ] = None,
    offset: Annotated[
        Optional[int],
        typer.Option("--offset", help="Порядковый номер первого счётчика (с 1)."),
    ] = None,
    all_pages: Annotated[
        bool,
        typer.Option("--all", help="Забрать все страницы (цикл по offset до rows)."),
    ] = False,
    counter_ids: Annotated[
        Optional[str],
        typer.Option("--counter-ids", help="ID счётчиков через запятую."),
    ] = None,
    favorite: Annotated[
        Optional[bool],
        typer.Option("--favorite/--no-favorite", help="Только избранные счётчики."),
    ] = None,
    field: Annotated[
        Optional[str],
        typer.Option(
            "--field",
            help="Доп. поля объекта через запятую: goals, mirrors, grants, filters, "
            "operations, counter_flags, measurement_tokens.",
        ),
    ] = None,
    label_id: Annotated[
        Optional[int], typer.Option("--label-id", help="Фильтр по метке.")
    ] = None,
    permission: Annotated[
        Optional[str],
        typer.Option(
            "--permission",
            help="Уровень доступа: own | view | edit | analyst | view_access_filter "
            "| analyst_access_filter (можно несколько через запятую).",
        ),
    ] = None,
    reverse: Annotated[
        Optional[bool],
        typer.Option("--reverse/--no-reverse", help="Обратный порядок сортировки."),
    ] = None,
    robots: Annotated[
        Optional[bool],
        typer.Option("--robots/--no-robots", help="Учитывать роботов (default true)."),
    ] = None,
    search_string: Annotated[
        Optional[str],
        typer.Option(
            "--search-string",
            help="Подстрока: ID, название, сайт или домен счётчика.",
        ),
    ] = None,
    sort: Annotated[
        Optional[str],
        typer.Option("--sort", help="Сортировка: None | Default | Visits."),
    ] = None,
    status: Annotated[
        Optional[str],
        typer.Option("--status", help="Статус: Active | Deleted."),
    ] = None,
    type: Annotated[
        Optional[str], typer.Option("--type", help="Тип: simple | partner.")
    ] = None,
) -> None:
    """Список доступных счётчиков."""
    render(
        ctx,
        _api(ctx).list(
            per_page=per_page,
            offset=offset,
            counter_ids=counter_ids,
            favorite=favorite,
            field=field,
            label_id=label_id,
            permission=permission,
            reverse=reverse,
            robots=robots,
            search_string=search_string,
            sort=sort,
            status=status,
            type=type,
            all_pages=all_pages,
            pretty=get_state(ctx).pretty,
        ),
    )


@app.command("get")
@handle_errors
def get(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    field: Annotated[
        Optional[str],
        typer.Option(
            "--field",
            help="Доп. поля объекта через запятую: goals, mirrors, grants, filters, "
            "operations, counter_flags, measurement_tokens.",
        ),
    ] = None,
) -> None:
    """Информация о счётчике."""
    render(
        ctx,
        _api(ctx).get(counter_id, field=field, pretty=get_state(ctx).pretty),
    )


@app.command("create")
@handle_errors
def create(
    ctx: typer.Context,
    data: str = typer.Option(..., "--data", help=DATA_HELP),
    field: Annotated[
        Optional[str],
        typer.Option(
            "--field",
            help="Доп. поля возвращаемого объекта через запятую.",
        ),
    ] = None,
    ytm: Annotated[
        Optional[bool],
        typer.Option("--ytm/--no-ytm", help="Использование системы управления тегами."),
    ] = None,
) -> None:
    """Создать счётчик (тело: {"counter": {...}})."""
    render(
        ctx,
        _api(ctx).create(
            parse_data(data), field=field, ytm=ytm, pretty=get_state(ctx).pretty
        ),
    )


@app.command("edit")
@handle_errors
def edit(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
    data: str = typer.Option(..., "--data", help=DATA_HELP),
    field: Annotated[
        Optional[str],
        typer.Option(
            "--field",
            help="Доп. поля возвращаемого объекта через запятую.",
        ),
    ] = None,
) -> None:
    """Изменить счётчик (тело: {"counter": {...}})."""
    render(
        ctx,
        _api(ctx).edit(
            counter_id, parse_data(data), field=field, pretty=get_state(ctx).pretty
        ),
    )


@app.command("delete")
@handle_errors
def delete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID счётчика."),
) -> None:
    """Удалить счётчик."""
    render(ctx, _api(ctx).delete(counter_id, pretty=get_state(ctx).pretty))


@app.command("undelete")
@handle_errors
def undelete(
    ctx: typer.Context,
    counter_id: int = typer.Argument(..., help="ID удалённого счётчика."),
) -> None:
    """Восстановить удалённый счётчик."""
    render(ctx, _api(ctx).undelete(counter_id, pretty=get_state(ctx).pretty))
