"""Изменение сегмента

PUT /management/v1/counter/{counterId}/apisegment/segment/{segmentId}
"""

from .._core import Endpoint, GROUP_SEGMENTS

ENDPOINT = Endpoint(
    GROUP_SEGMENTS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/apisegment/segment/{segmentId}",
    'Изменить сегмент (тело: {"segment": {...}})',
    path_params=("counterId", "segmentId"),
)
