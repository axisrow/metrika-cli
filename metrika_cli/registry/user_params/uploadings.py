"""Список загрузок параметров

GET /management/v1/counter/{counterId}/user_params/uploadings
"""

from .._core import Endpoint, GROUP_USER_PARAMS

ENDPOINT = Endpoint(
    GROUP_USER_PARAMS,
    "uploadings",
    "GET",
    "management/v1/counter/{counterId}/user_params/uploadings",
    "Список загрузок параметров посетителей",
    path_params=("counterId",),
)

# Query-параметры (openapi user_params/findAll): limit (default 10000),
# offset (default 0).
