"""Ресурс «Фильтры счётчика» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_FILTERS


class Filters(Resource):
    group = GROUP_FILTERS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def get(self, counter_id: int, filter_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "get",
            counterId=counter_id,
            filterId=filter_id,
            pretty=pretty,
        )

    def create(self, counter_id: int, filter_: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create",
            counterId=counter_id,
            json={"filter": filter_},
            pretty=pretty,
        )

    def edit(
        self,
        counter_id: int,
        filter_id: int,
        filter_: dict,
        *,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            filterId=filter_id,
            json={"filter": filter_},
            pretty=pretty,
        )

    def delete(self, counter_id: int, filter_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "delete",
            counterId=counter_id,
            filterId=filter_id,
            pretty=pretty,
        )
