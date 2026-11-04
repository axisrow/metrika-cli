"""Информация о цели

GET /management/v1/counter/{counterId}/goal/{goalId}
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/goal/{goalId}",
    "Информация о цели",
    path_params=("counterId", "goalId"),
)
