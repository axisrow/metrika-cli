"""Включить публичный доступ к счётчику (публичный просмотр статистики)

POST /management/v1/counter/{counterId}/public_grant

Подтверждено официальным openapi (management/openapi/grant/addPublicGrant.md,
«Создание публичного разрешения») и вендорным маппингом (методы POST/DELETE).
Расхождение с текстом issue 5: там для public_grant указаны GET/PUT — таких
методов в openapi нет.
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "public_set",
    "POST",
    "management/v1/counter/{counterId}/public_grant",
    "Включить публичный доступ к счётчику",
    path_params=("counterId",),
)
