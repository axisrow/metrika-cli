"""Удалить цель

DELETE /management/v1/counter/{counterId}/goal/{goalId}
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/goal/{goalId}",
    "Удалить цель",
    path_params=("counterId", "goalId"),
)
