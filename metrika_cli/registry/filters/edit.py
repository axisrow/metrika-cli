"""Изменить фильтр

PUT /management/v1/counter/{counterId}/filter/{filterId}
"""

from .._core import Endpoint, GROUP_FILTERS

ENDPOINT = Endpoint(
    GROUP_FILTERS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/filter/{filterId}",
    'Изменить фильтр (тело: {"filter": {...}})',
    path_params=("counterId", "filterId"),
)
