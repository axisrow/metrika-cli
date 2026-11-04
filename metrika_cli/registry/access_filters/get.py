"""Информация о фильтре доступа

GET /management/v1/counter/{counterId}/access_filter/{accessFilterId}
"""

from .._core import Endpoint, GROUP_ACCESS_FILTERS

ENDPOINT = Endpoint(
    GROUP_ACCESS_FILTERS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
    "Информация о фильтре доступа",
    path_params=("counterId", "accessFilterId"),
)
