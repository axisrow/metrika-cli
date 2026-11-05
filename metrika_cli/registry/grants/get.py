"""Информация о разрешении пользователя

GET /management/v1/counter/{counterId}/grant

Подтверждено официальным openapi (management/openapi/grant/grant.md,
ревизия r21770580): ``user_login`` — ОБЯЗАТЕЛЬНЫЙ query-параметр.
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "get",
    "GET",
    "management/v1/counter/{counterId}/grant",
    "Информация о разрешении пользователя",
    path_params=("counterId",),
)
