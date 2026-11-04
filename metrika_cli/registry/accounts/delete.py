"""Удалить аккаунт из списка доступных

DELETE /management/v1/account?user_login=<login>

В issue #6 операция не описана; есть в текущем openapi
(account/deleteAccount) и вендорном маппинге 2022. Путь — единственное
число, БЕЗ плейсхолдера: логин передаётся обязательным query-параметром
``user_login`` (по аналогии подтверждено страницей openapi).
"""

from .._core import Endpoint, GROUP_ACCOUNTS

ENDPOINT = Endpoint(
    GROUP_ACCOUNTS,
    "delete",
    "DELETE",
    "management/v1/account",
    "Удалить аккаунт (query: user_login)",
)
