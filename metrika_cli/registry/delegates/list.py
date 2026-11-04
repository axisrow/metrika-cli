"""Список представителей

GET /management/v1/delegates

Источник: openapi delegates/delegates (пути совпадают с вендорным
маппингом 2022, management/v1/delegates).
"""

from .._core import Endpoint, GROUP_DELEGATES

ENDPOINT = Endpoint(
    GROUP_DELEGATES,
    "list",
    "GET",
    "management/v1/delegates",
    "Список представителей",
)
