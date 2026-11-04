"""Сводная таблица

GET /stat/v1/data/pivot

Доп. параметр pivot_dimensions.
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "pivot",
    "GET",
    "stat/v1/data/pivot",
    "Сводная таблица (pivot_dimensions)",
)
