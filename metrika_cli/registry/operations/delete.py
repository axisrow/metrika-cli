"""Удалить операцию

DELETE /management/v1/counter/{counterId}/operation/{operationId}
"""

from .._core import Endpoint, GROUP_OPERATIONS

ENDPOINT = Endpoint(
    GROUP_OPERATIONS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/operation/{operationId}",
    "Удалить операцию",
    path_params=("counterId", "operationId"),
)
