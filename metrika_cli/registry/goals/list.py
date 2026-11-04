"""Список целей счётчика

GET /management/v1/counter/{counterId}/goals
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/goals",
    "Список целей счётчика",
    path_params=("counterId",),
)
