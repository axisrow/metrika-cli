"""Изменить список аккаунтов

PUT /management/v1/accounts

В issue #6 упомянут только list; PUT есть в текущем openapi
(account/updateAccounts) и вендорном маппинге 2022 (methods
GET/PUT/DELETE), поэтому реализован. Тело запроса {"accounts": [...]}.
"""

from .._core import Endpoint, GROUP_ACCOUNTS

ENDPOINT = Endpoint(
    GROUP_ACCOUNTS,
    "update",
    "PUT",
    "management/v1/accounts",
    'Изменить список аккаунтов (тело: {"accounts": [...]})',
)
