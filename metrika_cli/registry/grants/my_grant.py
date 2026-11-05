"""Разрешение текущего пользователя

GET /management/v1/counter/{counterId}/my_grant

Подтверждено официальным openapi (management/openapi/grant/myGrant.md,
ревизия r21770580).
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "my_grant",
    "GET",
    "management/v1/counter/{counterId}/my_grant",
    "Разрешение текущего пользователя",
    path_params=("counterId",),
)
