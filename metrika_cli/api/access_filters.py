"""Ресурс «Фильтры доступа» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_ACCESS_FILTERS


class AccessFilters(Resource):
    group = GROUP_ACCESS_FILTERS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def get(
        self, counter_id: int, access_filter_id: int, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "get",
            counterId=counter_id,
            accessFilterId=access_filter_id,
            pretty=pretty,
        )

    def create(
        self, counter_id: int, access_filter: dict, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "create",
            counterId=counter_id,
            json={"access_filter": access_filter},
            pretty=pretty,
        )

    def edit(
        self,
        counter_id: int,
        access_filter_id: int,
        access_filter: dict,
        *,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            accessFilterId=access_filter_id,
            json={"access_filter": access_filter},
            pretty=pretty,
        )

    def delete(
        self,
        counter_id: int,
        access_filter_id: int,
        *,
        delete_grants: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "delete",
            counterId=counter_id,
            accessFilterId=access_filter_id,
            params={"delete_grants": "true" if delete_grants else "false"},
            pretty=pretty,
        )
