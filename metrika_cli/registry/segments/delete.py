"""Удаление сегмента

DELETE /management/v1/counter/{counterId}/apisegment/segment/{segmentId}
"""

from .._core import Endpoint, GROUP_SEGMENTS

ENDPOINT = Endpoint(
    GROUP_SEGMENTS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/apisegment/segment/{segmentId}",
    "Удалить сегмент",
    path_params=("counterId", "segmentId"),
)
