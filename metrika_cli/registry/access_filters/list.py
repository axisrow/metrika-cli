"""Список фильтров доступа для счётчика

GET /management/v1/counter/{counterId}/access_filters
"""

from .._core import Endpoint, GROUP_ACCESS_FILTERS

ENDPOINT = Endpoint(
    GROUP_ACCESS_FILTERS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/access_filters",
    "Список фильтров доступа счётчика",
    path_params=("counterId",),
)
