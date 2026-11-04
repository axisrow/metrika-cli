"""Информация о примечании на графике счётчика

GET /management/v1/counter/{counterId}/chart_annotation/{id}
"""

from .._core import Endpoint, GROUP_ANNOTATIONS

ENDPOINT = Endpoint(
    GROUP_ANNOTATIONS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/chart_annotation/{id}",
    "Информация о примечании на графике счётчика",
    path_params=("counterId", "id"),
)
