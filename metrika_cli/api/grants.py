"""Ресурс «Доступы к счётчику» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_GRANTS


class Grants(Resource):
    group = GROUP_GRANTS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def create(self, counter_id: int, grant: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create", counterId=counter_id, json={"grant": grant}, pretty=pretty
        )

    def delete(self, counter_id: int, user_login: str, *, pretty: bool = False) -> Any:
        return self._call(
            "delete",
            counterId=counter_id,
            params={"user_login": user_login},
            pretty=pretty,
        )

    def public_set(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("public_set", counterId=counter_id, pretty=pretty)

    def public_delete(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("public_delete", counterId=counter_id, pretty=pretty)
