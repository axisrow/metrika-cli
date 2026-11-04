"""Удалить фильтр

DELETE /management/v1/counter/{counterId}/filter/{filterId}
"""

from .._core import Endpoint, GROUP_FILTERS

ENDPOINT = Endpoint(
    GROUP_FILTERS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/filter/{filterId}",
    "Удалить фильтр",
    path_params=("counterId", "filterId"),
)
