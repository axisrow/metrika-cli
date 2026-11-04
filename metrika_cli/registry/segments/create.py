"""Создание сегмента

POST /management/v1/counter/{counterId}/apisegment/segments
"""

from .._core import Endpoint, GROUP_SEGMENTS

ENDPOINT = Endpoint(
    GROUP_SEGMENTS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/apisegment/segments",
    'Создать сегмент (тело: {"segment": {...}})',
    path_params=("counterId",),
)
