"""Создать счётчик

POST /management/v1/counters
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "create",
    "POST",
    "management/v1/counters",
    'Создать счётчик (тело: {"counter": {...}})',
)
