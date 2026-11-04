"""Удаление фильтра доступа

DELETE /management/v1/counter/{counterId}/access_filter/{accessFilterId}

Query-параметр ``delete_grants`` (по умолчанию false) — удалить также
связанные гранты на этот фильтр.
"""

from .._core import Endpoint, GROUP_ACCESS_FILTERS

ENDPOINT = Endpoint(
    GROUP_ACCESS_FILTERS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/access_filter/{accessFilterId}",
    "Удалить фильтр доступа",
    path_params=("counterId", "accessFilterId"),
)
