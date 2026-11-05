"""Команды группы ``stat`` (Reports API: table/bytime/comparison/drilldown/pivot
и comparison_drilldown)."""

from __future__ import annotations

from typing import Annotated, Optional

import typer

from ..api.stat import Stat
from ..context import get_state, handle_errors
from ..render import render

app = typer.Typer(help="Отчёты (Reports API, /stat/v1).", no_args_is_help=True)

# Общие опции отчёта (до 20 метрик / 10 группировок; limit ≤100000; offset с 1).
IDS = Annotated[str, typer.Option("--ids", help="ID счётчиков через запятую.")]
METRICS = Annotated[
    str, typer.Option("--metrics", help="Метрики через запятую (ym:s:visits…).")
]
DIMENSIONS = Annotated[
    Optional[str], typer.Option("--dimensions", help="Группировки через запятую (≤10).")
]
DATE1 = Annotated[
    Optional[str], typer.Option("--date1", help="Начало периода (YYYY-MM-DD).")
]
DATE2 = Annotated[Optional[str], typer.Option("--date2", help="Конец периода.")]
FILTERS = Annotated[
    Optional[str],
    typer.Option("--filters", help="Фильтр-выражение: ym:s:pageViews>5, …"),
]
SORT = Annotated[
    Optional[str], typer.Option("--sort", help="Сортировка: -ym:s:visits…")
]
LIMIT = Annotated[
    Optional[int], typer.Option("--limit", help="Строк на страницу (≤100000).")
]
OFFSET = Annotated[Optional[int], typer.Option("--offset", help="Смещение (с 1).")]
PRESET = Annotated[
    Optional[str],
    typer.Option("--preset", help="Пресет отчёта, напр. sources_summary."),
]
LANG = Annotated[
    Optional[str], typer.Option("--lang", help="Язык значений группировок (ru/en…).")
]
CSV = Annotated[bool, typer.Option("--csv", help="Ответ CSV вместо JSON.")]

# Семплирование и окружение (общие для всех 6 операций, openapi stat).
ACCURACY = Annotated[
    Optional[str],
    typer.Option("--accuracy", help="Размер выборки (семплирование)."),
]
PROPOSED_ACCURACY = Annotated[
    Optional[bool],
    typer.Option(
        "--proposed-accuracy",
        help="Разрешить API поднять accuracy до рекомендованного.",
    ),
]
TIMEZONE = Annotated[
    Optional[str],
    typer.Option("--timezone", help="Часовой пояс выборки в формате ±hh:mm."),
]
INCLUDE_UNDEFINED = Annotated[
    Optional[bool],
    typer.Option(
        "--include-undefined",
        help="Включить строки с неопределённым значением первой группировки.",
    ),
]
DIRECT_CLIENT_LOGINS = Annotated[
    Optional[str],
    typer.Option(
        "--direct-client-logins",
        help="Логины клиентов Директа через запятую (отчёт Директ-расходы).",
    ),
]


def _api(ctx: typer.Context) -> Stat:
    return Stat(get_state(ctx).client())


def _emit(ctx: typer.Context, data, csv: bool) -> None:
    if csv:
        typer.echo(data)
        return
    render(ctx, data)


@app.command("table")
@handle_errors
def table(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    dimensions: DIMENSIONS = None,
    date1: DATE1 = None,
    date2: DATE2 = None,
    filters: FILTERS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    csv: CSV = False,
) -> None:
    """Сводная таблица: метрики × группировки."""
    _emit(
        ctx,
        _api(ctx).table(
            ids=ids,
            metrics=metrics,
            dimensions=dimensions,
            date1=date1,
            date2=date2,
            filters=filters,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            csv=csv,
        ),
        csv,
    )


@app.command("bytime")
@handle_errors
def bytime(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    group: Annotated[
        Optional[str], typer.Option("--group", help="day | week | dekadam | month.")
    ] = None,
    dimensions: DIMENSIONS = None,
    date1: DATE1 = None,
    date2: DATE2 = None,
    filters: FILTERS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    top_keys: Annotated[
        Optional[str],
        typer.Option(
            "--top-keys",
            help="Число строк, если не задан --row-ids (макс. 30, default 7).",
        ),
    ] = None,
    row_ids: Annotated[
        Optional[str],
        typer.Option(
            "--row-ids",
            help="Выбор строк для графиков (перечисление списков ключей, формат API).",
        ),
    ] = None,
    include_annotations: Annotated[
        Optional[bool],
        typer.Option("--include-annotations", help="Включить примечания в ответ."),
    ] = None,
    annotation_groups: Annotated[
        Optional[str],
        typer.Option(
            "--annotation-groups",
            help="Группы примечаний через запятую (при --include-annotations).",
        ),
    ] = None,
    keys_sort: Annotated[
        Optional[str],
        typer.Option(
            "--keys-sort",
            help="Сортировка по группировкам/метрикам через запятую («-» — по убыванию).",
        ),
    ] = None,
    csv: CSV = False,
) -> None:
    """Динамика метрик по времени."""
    _emit(
        ctx,
        _api(ctx).bytime(
            ids=ids,
            metrics=metrics,
            group=group,
            dimensions=dimensions,
            date1=date1,
            date2=date2,
            filters=filters,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            top_keys=top_keys,
            row_ids=row_ids,
            include_annotations=include_annotations,
            annotation_groups=annotation_groups,
            keys_sort=keys_sort,
            csv=csv,
        ),
        csv,
    )


@app.command("comparison")
@handle_errors
def comparison(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    date1_a: Annotated[Optional[str], typer.Option(help="Период A: начало.")] = None,
    date2_a: Annotated[Optional[str], typer.Option(help="Период A: конец.")] = None,
    date1_b: Annotated[Optional[str], typer.Option(help="Период B: начало.")] = None,
    date2_b: Annotated[Optional[str], typer.Option(help="Период B: конец.")] = None,
    filters_a: Annotated[Optional[str], typer.Option(help="Сегмент A.")] = None,
    filters_b: Annotated[Optional[str], typer.Option(help="Сегмент B.")] = None,
    dimensions: DIMENSIONS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    csv: CSV = False,
) -> None:
    """Сравнение периодов (date*_a vs date*_b) или сегментов (filters_a vs filters_b)."""
    _emit(
        ctx,
        _api(ctx).comparison(
            ids=ids,
            metrics=metrics,
            date1_a=date1_a,
            date2_a=date2_a,
            date1_b=date1_b,
            date2_b=date2_b,
            filters_a=filters_a,
            filters_b=filters_b,
            dimensions=dimensions,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            csv=csv,
        ),
        csv,
    )


@app.command("drilldown")
@handle_errors
def drilldown(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    dimensions: Annotated[
        str, typer.Option("--dimensions", help="Иерархия группировок (≤10).")
    ],
    parent_id: Annotated[
        Optional[str], typer.Option("--parent-id", help="ID узла для разворачивания.")
    ] = None,
    date1: DATE1 = None,
    date2: DATE2 = None,
    filters: FILTERS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    only_expandable_undefined: Annotated[
        Optional[bool],
        typer.Option(
            "--only-expandable-undefined",
            help="Строки «не определено» только для разворачиваемых группировок.",
        ),
    ] = None,
    csv: CSV = False,
) -> None:
    """Иерархический отчёт (drill down; фильтровать по ID, не по именам)."""
    _emit(
        ctx,
        _api(ctx).drilldown(
            ids=ids,
            metrics=metrics,
            dimensions=dimensions,
            parent_id=parent_id,
            date1=date1,
            date2=date2,
            filters=filters,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            only_expandable_undefined=only_expandable_undefined,
            csv=csv,
        ),
        csv,
    )


@app.command("comparison-drilldown")
@handle_errors
def comparison_drilldown(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    date1_a: Annotated[Optional[str], typer.Option(help="Период A: начало.")] = None,
    date2_a: Annotated[Optional[str], typer.Option(help="Период A: конец.")] = None,
    date1_b: Annotated[Optional[str], typer.Option(help="Период B: начало.")] = None,
    date2_b: Annotated[Optional[str], typer.Option(help="Период B: конец.")] = None,
    filters_a: Annotated[Optional[str], typer.Option(help="Сегмент A.")] = None,
    filters_b: Annotated[Optional[str], typer.Option(help="Сегмент B.")] = None,
    parent_id: Annotated[
        Optional[str], typer.Option("--parent-id", help="ID узла для разворачивания.")
    ] = None,
    dimensions: DIMENSIONS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    only_expandable_undefined: Annotated[
        Optional[bool],
        typer.Option(
            "--only-expandable-undefined",
            help="Строки «не определено» только для разворачиваемых группировок.",
        ),
    ] = None,
    csv: CSV = False,
) -> None:
    """Сравнение периодов/сегментов по дереву группировок (drill down)."""
    _emit(
        ctx,
        _api(ctx).comparison_drilldown(
            ids=ids,
            metrics=metrics,
            dimensions=dimensions,
            date1_a=date1_a,
            date2_a=date2_a,
            date1_b=date1_b,
            date2_b=date2_b,
            filters_a=filters_a,
            filters_b=filters_b,
            parent_id=parent_id,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            only_expandable_undefined=only_expandable_undefined,
            csv=csv,
        ),
        csv,
    )


@app.command("pivot")
@handle_errors
def pivot(
    ctx: typer.Context,
    ids: IDS,
    metrics: METRICS,
    dimensions: Annotated[str, typer.Option("--dimensions", help="Группировки (≤10).")],
    pivot_dimensions: Annotated[
        str, typer.Option("--pivot-dimensions", help="Размерности разворота.")
    ],
    date1: DATE1 = None,
    date2: DATE2 = None,
    filters: FILTERS = None,
    sort: SORT = None,
    limit: LIMIT = None,
    offset: OFFSET = None,
    preset: PRESET = None,
    lang: LANG = None,
    accuracy: ACCURACY = None,
    proposed_accuracy: PROPOSED_ACCURACY = None,
    timezone: TIMEZONE = None,
    include_undefined: INCLUDE_UNDEFINED = None,
    direct_client_logins: DIRECT_CLIENT_LOGINS = None,
    pivot_limit: Annotated[
        Optional[int], typer.Option("--pivot-limit", help="Лимит строк разворота.")
    ] = None,
    pivot_offset: Annotated[
        Optional[int], typer.Option("--pivot-offset", help="Смещение строк разворота.")
    ] = None,
    csv: CSV = False,
) -> None:
    """Сводная таблица (pivot)."""
    _emit(
        ctx,
        _api(ctx).pivot(
            ids=ids,
            metrics=metrics,
            dimensions=dimensions,
            pivot_dimensions=pivot_dimensions,
            date1=date1,
            date2=date2,
            filters=filters,
            sort=sort,
            limit=limit,
            offset=offset,
            preset=preset,
            lang=lang,
            accuracy=accuracy,
            proposed_accuracy=proposed_accuracy,
            timezone=timezone,
            include_undefined=include_undefined,
            direct_client_logins=direct_client_logins,
            pivot_limit=pivot_limit,
            pivot_offset=pivot_offset,
            csv=csv,
        ),
        csv,
    )
