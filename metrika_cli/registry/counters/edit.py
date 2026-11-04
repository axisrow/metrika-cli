"""Изменить счётчик

PUT /management/v1/counter/{counterId}
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}",
    'Изменить счётчик (тело: {"counter": {...}})',
    path_params=("counterId",),
)
