"""Список доступов к счётчику

GET /management/v1/counter/{counterId}/grants

Подтверждено официальным openapi (management/openapi/grant/grants.md) и
вендорным маппингом (``_resource_mapping.py``).
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "list",
    "GET",
    "management/v1/counter/{counterId}/grants",
    "Список доступов к счётчику",
    path_params=("counterId",),
)
