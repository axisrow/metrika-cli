"""Изменить примечание на графике счётчика

PUT /management/v1/counter/{counterId}/chart_annotation/{id}
"""

from .._core import Endpoint, GROUP_ANNOTATIONS

ENDPOINT = Endpoint(
    GROUP_ANNOTATIONS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/chart_annotation/{id}",
    "Изменить примечание на графике счётчика",
    path_params=("counterId", "id"),
)
