"""Удалить счётчик

DELETE /management/v1/counter/{counterId}
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}",
    "Удалить счётчик",
    path_params=("counterId",),
)
