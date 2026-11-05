"""Ресурс «Счётчики» (Management API) — 6 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
Query-параметры list/get/create/edit сверены с официальным openapi
(management/openapi/counter/*.md, ревизия r21770580, 2026-11-05).
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_COUNTERS


class Counters(Resource):
    group = GROUP_COUNTERS

    def list(
        self,
        *,
        per_page: Optional[int] = None,
        offset: Optional[int] = None,
        counter_ids: Optional[str] = None,
        favorite: Optional[bool] = None,
        field: Optional[str] = None,
        label_id: Optional[int] = None,
        permission: Optional[str] = None,
        reverse: Optional[bool] = None,
        robots: Optional[bool] = None,
        search_string: Optional[str] = None,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002 — имя query-параметра API
        all_pages: bool = False,
        pretty: bool = False,
    ) -> Any:
        """Список счётчиков; per_page (≤10000, default 1000) и offset (с 1).

        Фильтры (counter_ids, favorite, field, label_id, permission, reverse,
        robots, search_string, sort, status, type) применяются к каждой
        странице при ``all_pages``.
        """
        counters: list = []
        result: Any = {}
        page = 1 if offset is None else offset
        filters = {
            k: v
            for k, v in (
                ("counter_ids", counter_ids),
                ("favorite", favorite),
                ("field", field),
                ("label_id", label_id),
                ("permission", permission),
                ("reverse", reverse),
                ("robots", robots),
                ("search_string", search_string),
                ("sort", sort),
                ("status", status),
                ("type", type),
            )
            if v is not None
        }
        while True:
            params: dict = {"offset": page}
            if per_page is not None:
                params["per_page"] = per_page
            params.update(filters)
            result = self._call("list", params=params, pretty=pretty)
            chunk = result.get("counters") or []
            counters.extend(chunk)
            total = result.get("rows")
            # стоп: без --all, пустая страница, нет rows в ответе или всё собрали
            if not all_pages or not chunk or total is None or len(counters) >= total:
                break
            page += len(chunk)
        result["counters"] = counters
        return result

    def get(
        self, counter_id: int, *, field: Optional[str] = None, pretty: bool = False
    ) -> Any:
        params = {"field": field} if field else None
        return self._call("get", counterId=counter_id, params=params, pretty=pretty)

    def create(
        self,
        counter: dict,
        *,
        field: Optional[str] = None,
        ytm: Optional[bool] = None,
        pretty: bool = False,
    ) -> Any:
        params = {
            k: v for k, v in (("field", field), ("ytm", ytm)) if v is not None
        }
        return self._call(
            "create", json={"counter": counter}, params=params or None, pretty=pretty
        )

    def edit(
        self,
        counter_id: int,
        counter: dict,
        *,
        field: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            json={"counter": counter},
            params={"field": field} if field else None,
            pretty=pretty,
        )

    def delete(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("delete", counterId=counter_id, pretty=pretty)

    def undelete(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("undelete", counterId=counter_id, pretty=pretty)
