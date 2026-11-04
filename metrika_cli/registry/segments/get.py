"""Информация о сегменте

GET /management/v1/counter/{counterId}/apisegment/segment/{segmentId}
"""

from .._core import Endpoint, GROUP_SEGMENTS

ENDPOINT = Endpoint(
    GROUP_SEGMENTS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/apisegment/segment/{segmentId}",
    "Информация о сегменте",
    path_params=("counterId", "segmentId"),
)
