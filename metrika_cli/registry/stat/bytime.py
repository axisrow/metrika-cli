"""Отчёт по времени

GET /stat/v1/data/bytime

Как table, плюс group=day|week|dekamonth|month.
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "bytime",
    "GET",
    "stat/v1/data/bytime",
    "Динамика метрик по времени (group=day|week|month…)",
)
