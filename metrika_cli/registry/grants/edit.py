"""Изменение разрешения пользователя

PUT /management/v1/counter/{counterId}/grant

Подтверждено официальным openapi (management/openapi/grant/editGrant.md,
ревизия r21770580): тело {"grant": {...}} — user_login, perm, comment,
partner_data_access.
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "edit",
    "PUT",
    "management/v1/counter/{counterId}/grant",
    "Изменить разрешение пользователя",
    path_params=("counterId",),
)
