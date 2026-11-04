"""Изменить операцию

PUT /management/v1/counter/{counterId}/operation/{operationId}
"""

from .._core import Endpoint, GROUP_OPERATIONS

ENDPOINT = Endpoint(
    GROUP_OPERATIONS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/operation/{operationId}",
    'Изменить операцию (тело: {"operation": {...}})',
    path_params=("counterId", "operationId"),
)
