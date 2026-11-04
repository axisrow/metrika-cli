"""Создать цель

POST /management/v1/counter/{counterId}/goals
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/goals",
    'Создать цель (тело: {"goal": {...}})',
    path_params=("counterId",),
)
