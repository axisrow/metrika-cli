"""Создать примечание на графике счётчика

POST /management/v1/counter/{counterId}/chart_annotations
"""

from .._core import Endpoint, GROUP_ANNOTATIONS

ENDPOINT = Endpoint(
    GROUP_ANNOTATIONS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/chart_annotations",
    "Создать примечание на графике счётчика",
    path_params=("counterId",),
)
