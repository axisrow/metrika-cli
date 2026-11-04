"""Сравнение деревьев drill down

GET /stat/v1/data/comparison/drilldown

Сравнение двух периодов/сегментов (…_a vs …_b) по дереву группировок.
Путь (через слэш, не «comparison_drilldown») подтверждён openapi-справочником
stat: страница «Сравнение - drill down» (stat/openapi/comparison_drilldown.md).
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "comparison_drilldown",
    "GET",
    "stat/v1/data/comparison/drilldown",
    "Сравнение периодов/сегментов по дереву группировок (drill down)",
)
