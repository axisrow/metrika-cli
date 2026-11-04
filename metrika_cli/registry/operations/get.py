"""Получить операцию

GET /management/v1/counter/{counterId}/operation/{operationId}
"""

from .._core import Endpoint, GROUP_OPERATIONS

ENDPOINT = Endpoint(
    GROUP_OPERATIONS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/operation/{operationId}",
    "Информация об операции",
    path_params=("counterId", "operationId"),
)
