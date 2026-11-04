"""Список фильтров счётчика

GET /management/v1/counter/{counterId}/filters
"""

from .._core import Endpoint, GROUP_FILTERS

ENDPOINT = Endpoint(
    GROUP_FILTERS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/filters",
    "Список фильтров счётчика (не более 30 на счётчик)",
    path_params=("counterId",),
)
