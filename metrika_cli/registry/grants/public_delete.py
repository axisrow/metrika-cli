"""Выключить публичный доступ к счётчику

DELETE /management/v1/counter/{counterId}/public_grant

Подтверждено официальным openapi (management/openapi/grant/deletePublicGrant.md,
«Удаление публичного разрешения») и вендорным маппингом. В issue 5 для этой
пары фигурировал GET (op ``public_get``) — GET на public_grant в openapi
отсутствует, поэтому op назван ``public_delete`` (unverified-метод не заводим).
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "public_delete",
    "DELETE",
    "management/v1/counter/{counterId}/public_grant",
    "Выключить публичный доступ к счётчику",
    path_params=("counterId",),
)
