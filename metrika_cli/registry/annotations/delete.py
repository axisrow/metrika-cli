"""Удалить примечание на графике счётчика

DELETE /management/v1/counter/{counterId}/chart_annotation/{id}
"""

from .._core import Endpoint, GROUP_ANNOTATIONS

ENDPOINT = Endpoint(
    GROUP_ANNOTATIONS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/chart_annotation/{id}",
    "Удалить примечание на графике счётчика",
    path_params=("counterId", "id"),
)
