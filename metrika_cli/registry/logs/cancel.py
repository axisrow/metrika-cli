"""Отменить необработанный лог-запрос

POST /management/v1/counter/{counterId}/logrequest/{requestId}/cancel
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "cancel",
    "POST",
    "management/v1/counter/{counterId}/logrequest/{requestId}/cancel",
    "Отменить запрос в статусе created",
    path_params=("counterId", "requestId"),
)
