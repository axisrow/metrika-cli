"""Создать фильтр

POST /management/v1/counter/{counterId}/filters
"""

from .._core import Endpoint, GROUP_FILTERS

ENDPOINT = Endpoint(
    GROUP_FILTERS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/filters",
    'Создать фильтр (тело: {"filter": {...}})',
    path_params=("counterId",),
)
