"""Информация о загрузке офлайн-звонков по ID

GET /management/v1/counter/{counterId}/offline_conversions/calls_uploading/{id}
"""

from .._core import Endpoint, GROUP_CALLS

ENDPOINT = Endpoint(
    GROUP_CALLS,
    "uploading",
    "GET",
    "management/v1/counter/{counterId}/offline_conversions/calls_uploading/{id}",
    "Информация о загрузке звонков по ID",
    path_params=("counterId", "id"),
)
