"""Отозвать доступ пользователя к счётчику

DELETE /management/v1/counter/{counterId}/grant

Подтверждено официальным openapi (management/openapi/grant/deleteGrant.md)
и вендорным маппингом: ``user_login`` (или ``user_uid``) — query-параметр,
НЕ сегмент пути ``/grant/{userLogin}`` (так в тексте issue 5).
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "delete",
    "DELETE",
    "management/v1/counter/{counterId}/grant",
    "Отозвать доступ пользователя",
    path_params=("counterId",),
)
