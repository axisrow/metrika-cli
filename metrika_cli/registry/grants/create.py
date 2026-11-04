"""Выдать доступ пользователю к счётчику

POST /management/v1/counter/{counterId}/grants

Подтверждено официальным openapi (management/openapi/grant/addGrant.md):
тело ``{"grant": {...}}``, ``perm`` ∈ public_stat | view | edit | analyst |
analyst_access_filter. Совпадает с вендорным маппингом.
"""

from .._core import Endpoint, GROUP_GRANTS

ENDPOINT = Endpoint(
    GROUP_GRANTS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/grants",
    'Выдать доступ пользователю (тело: {"grant": {...}})',
    path_params=("counterId",),
)
