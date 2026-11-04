"""Сравнение сегментов/периодов

GET /stat/v1/data/comparison

Варианты: date1_a/date2_a vs date1_b/date2_b, либо filters_a vs filters_b.
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "comparison",
    "GET",
    "stat/v1/data/comparison",
    "Сравнение двух периодов или сегментов (…_a vs …_b)",
)
