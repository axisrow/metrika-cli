"""Освободить квоту: убрать выгрузку обработанного запроса

POST /management/v1/counter/{counterId}/logrequest/{requestId}/clean
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "clean",
    "POST",
    "management/v1/counter/{counterId}/logrequest/{requestId}/clean",
    "Удалить подготовленные части (освободить 10 ГБ квоту счётчика)",
    path_params=("counterId", "requestId"),
)
