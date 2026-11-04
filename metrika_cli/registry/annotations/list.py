"""Список примечаний на графиках счётчика

GET /management/v1/counter/{counterId}/chart_annotations
"""

from .._core import Endpoint, GROUP_ANNOTATIONS

ENDPOINT = Endpoint(
    GROUP_ANNOTATIONS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/chart_annotations",
    "Список примечаний на графиках счётчика",
    path_params=("counterId",),
)
