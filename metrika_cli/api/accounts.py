"""Ресурс «Аккаунты» (Management API) — 3 эндпоинта.

list обязателен по issue #6; update/delete добавлены по текущему openapi
(account/updateAccounts, account/deleteAccount) и вендорному маппингу
2022 (methods GET/PUT/DELETE).
"""

from __future__ import annotations

from typing import Any, List

from ..base import Resource
from ..registry import GROUP_ACCOUNTS


class Accounts(Resource):
    group = GROUP_ACCOUNTS

    def list(self, *, pretty: bool = False) -> Any:
        return self._call("list", pretty=pretty)

    def update(self, accounts: List[dict], *, pretty: bool = False) -> Any:
        return self._call("update", json={"accounts": accounts}, pretty=pretty)

    def delete(self, user_login: str, *, pretty: bool = False) -> Any:
        """Логин удаляемого передаётся query-параметром (openapi, см. registry)."""
        return self._call("delete", params={"user_login": user_login}, pretty=pretty)
