"""Создать операцию

POST /management/v1/counter/{counterId}/operations
"""

from .._core import Endpoint, GROUP_OPERATIONS

ENDPOINT = Endpoint(
    GROUP_OPERATIONS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/operations",
    'Создать операцию (тело: {"operation": {...}})',
    path_params=("counterId",),
)
