"""Список счётчиков пользователя

GET /management/v1/counters
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "list",
    "GET",
    "management/v1/counters",
    "Список доступных счётчиков",
)
