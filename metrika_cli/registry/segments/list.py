"""Список сегментов для счетчика

GET /management/v1/counter/{counterId}/apisegment/segments
"""

from .._core import Endpoint, GROUP_SEGMENTS

ENDPOINT = Endpoint(
    GROUP_SEGMENTS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/apisegment/segments",
    "Список сегментов счётчика, созданных через API",
    path_params=("counterId",),
)
