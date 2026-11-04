"""Получить фильтр

GET /management/v1/counter/{counterId}/filter/{filterId}
"""

from .._core import Endpoint, GROUP_FILTERS

ENDPOINT = Endpoint(
    GROUP_FILTERS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/filter/{filterId}",
    "Информация о фильтре",
    path_params=("counterId", "filterId"),
)
