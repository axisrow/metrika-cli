"""Статус лог-запроса (poll)

GET /management/v1/counter/{counterId}/logrequest/{requestId}
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "info",
    "GET",
    "management/v1/counter/{counterId}/logrequest/{requestId}",
    "Статус запроса и список частей (parts)",
    path_params=("counterId", "requestId"),
)
