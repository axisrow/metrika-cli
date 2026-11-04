"""Отчёт-таблица

GET /stat/v1/data (CSV: /stat/v1/data.csv)

Параметры: ids, metrics (≤20), dimensions (≤10), date1/date2, filters,
sort, limit (≤100000, default 100), offset (с 1), preset, lang.
Префиксы ym:s:/ym:pv: смешивать нельзя.
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "table",
    "GET",
    "stat/v1/data",
    "Сводная таблица: метрики × группировки",
)
