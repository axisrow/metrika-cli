"""Список операций счётчика

GET /management/v1/counter/{counterId}/operations
"""

from .._core import Endpoint, GROUP_OPERATIONS

ENDPOINT = Endpoint(
    GROUP_OPERATIONS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/operations",
    "Список операций счётчика",
    path_params=("counterId",),
)
