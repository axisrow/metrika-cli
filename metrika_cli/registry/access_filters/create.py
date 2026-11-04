"""Создание фильтра доступа

POST /management/v1/counter/{counterId}/access_filters
"""

from .._core import Endpoint, GROUP_ACCESS_FILTERS

ENDPOINT = Endpoint(
    GROUP_ACCESS_FILTERS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/access_filters",
    'Создать фильтр доступа (тело: {"access_filter": {...}})',
    path_params=("counterId",),
)
