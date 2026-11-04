"""Изменить цель

PUT /management/v1/counter/{counterId}/goal/{goalId}
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/goal/{goalId}",
    'Изменить цель (тело: {"goal": {...}})',
    path_params=("counterId", "goalId"),
)
