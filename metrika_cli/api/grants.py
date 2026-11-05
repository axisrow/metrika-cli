"""Ресурс «Доступы к счётчику» (Management API) — 8 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
``user_uid`` в delete — альтернатива ``user_login`` (openapi deleteGrant.md).
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_GRANTS


class Grants(Resource):
    group = GROUP_GRANTS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def get(
        self, counter_id: int, user_login: str, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "get",
            counterId=counter_id,
            params={"user_login": user_login},
            pretty=pretty,
        )

    def create(self, counter_id: int, grant: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create", counterId=counter_id, json={"grant": grant}, pretty=pretty
        )

    def edit(self, counter_id: int, grant: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "edit", counterId=counter_id, json={"grant": grant}, pretty=pretty
        )

    def delete(
        self,
        counter_id: int,
        user_login: Optional[str] = None,
        *,
        user_uid: Optional[int] = None,
        pretty: bool = False,
    ) -> Any:
        params = {
            k: v
            for k, v in (("user_login", user_login), ("user_uid", user_uid))
            if v is not None
        }
        return self._call(
            "delete", counterId=counter_id, params=params, pretty=pretty
        )

    def my_grant(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("my_grant", counterId=counter_id, pretty=pretty)

    def public_set(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("public_set", counterId=counter_id, pretty=pretty)

    def public_delete(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("public_delete", counterId=counter_id, pretty=pretty)
