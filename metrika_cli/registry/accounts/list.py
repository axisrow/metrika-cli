"""Список аккаунтов пользователя

GET /management/v1/accounts

Источник: openapi account/accounts (путь совпадает с вендорным
маппингом 2022).
"""

from .._core import Endpoint, GROUP_ACCOUNTS

ENDPOINT = Endpoint(
    GROUP_ACCOUNTS,
    "list",
    "GET",
    "management/v1/accounts",
    "Список аккаунтов пользователя",
)
