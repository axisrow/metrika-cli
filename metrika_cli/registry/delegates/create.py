"""Добавить представителя

POST /management/v1/delegates

Источник: openapi delegates/addDelegate (путь совпадает с вендорным
маппингом 2022; тело запроса {"delegate": {...}}).
"""

from .._core import Endpoint, GROUP_DELEGATES

ENDPOINT = Endpoint(
    GROUP_DELEGATES,
    "create",
    "POST",
    "management/v1/delegates",
    'Добавить представителя (тело: {"delegate": {...}})',
)
