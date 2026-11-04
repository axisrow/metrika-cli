"""Информация о загрузке офлайн-конверсий

GET /management/v1/counter/{counterId}/offline_conversions/uploading/{id}
"""

from .._core import Endpoint, GROUP_CONVERSIONS

ENDPOINT = Endpoint(
    GROUP_CONVERSIONS,
    "uploading",
    "GET",
    "management/v1/counter/{counterId}/offline_conversions/uploading/{id}",
    "Информация о загрузке офлайн-конверсий по ID",
    path_params=("counterId", "id"),
)

# Query-параметры (openapi offline_conversions/findById_1): type
# (BASIC default | CALLS | CHATS).
