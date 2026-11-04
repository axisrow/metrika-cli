"""Ресурс «Представители» (Management API) — 3 эндпоинта.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_DELEGATES


class Delegates(Resource):
    group = GROUP_DELEGATES

    def list(self, *, pretty: bool = False) -> Any:
        return self._call("list", pretty=pretty)

    def create(self, delegate: dict, *, pretty: bool = False) -> Any:
        return self._call("create", json={"delegate": delegate}, pretty=pretty)

    def delete(self, user_login: str, *, pretty: bool = False) -> Any:
        """Логин удаляемого передаётся query-параметром (openapi, см. registry)."""
        return self._call("delete", params={"user_login": user_login}, pretty=pretty)
