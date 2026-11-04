"""Изменение фильтра доступа

PUT /management/v1/counter/{counterId}/access_filter/{accessFilterId}
"""

from .._core import Endpoint, GROUP_ACCESS_FILTERS

ENDPOINT = Endpoint(
    GROUP_ACCESS_FILTERS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
    'Изменить фильтр доступа (тело: {"access_filter": {...}})',
    path_params=("counterId", "accessFilterId"),
)
