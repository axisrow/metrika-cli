"""Список лог-запросов счётчика

GET /management/v1/counter/{counterId}/logrequests
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/logrequests",
    "Список лог-запросов (статусы, parts)",
    path_params=("counterId",),
)
