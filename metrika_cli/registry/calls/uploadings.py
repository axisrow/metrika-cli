"""Список загрузок офлайн-звонков

GET /management/v1/counter/{counterId}/offline_conversions/calls_uploadings
"""

from .._core import Endpoint, GROUP_CALLS

ENDPOINT = Endpoint(
    GROUP_CALLS,
    "uploadings",
    "GET",
    "management/v1/counter/{counterId}/offline_conversions/calls_uploadings",
    "Список загрузок звонков",
    path_params=("counterId",),
)

# Query-параметры (openapi call/findAllCallUploadings): limit (default
# 10000), offset (default 0).
