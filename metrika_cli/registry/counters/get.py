"""Получить счётчик

GET /management/v1/counter/{counterId}
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "get",
    "GET",
    "management/v1/counter/{counterId}",
    "Информация о счётчике",
    path_params=("counterId",),
)
