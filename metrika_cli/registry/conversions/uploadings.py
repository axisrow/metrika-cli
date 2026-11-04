"""Список загрузок офлайн-конверсий

GET /management/v1/counter/{counterId}/offline_conversions/uploadings
"""

from .._core import Endpoint, GROUP_CONVERSIONS

ENDPOINT = Endpoint(
    GROUP_CONVERSIONS,
    "uploadings",
    "GET",
    "management/v1/counter/{counterId}/offline_conversions/uploadings",
    "Список загрузок офлайн-конверсий",
    path_params=("counterId",),
)

# Query-параметры (openapi offline_conversions/findAll_1): limit (default
# 10000), offset (default 0), type (BASIC default | CALLS | CHATS).
