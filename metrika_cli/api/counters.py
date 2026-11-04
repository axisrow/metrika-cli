"""Ресурс «Счётчики» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
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
        all_pages: bool = False,
        pretty: bool = False,
    ) -> Any:
        """Список счётчиков; per_page (≤10000, default 1000) и offset (с 1).

        ``all_pages`` — забрать все страницы (по ``rows`` из ответа).
        """
        counters: list = []
        result: Any = {}
        page = 1 if offset is None else offset
        while True:
            params: dict = {"offset": page}
            if per_page is not None:
                params["per_page"] = per_page
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

    def get(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("get", counterId=counter_id, pretty=pretty)

    def create(self, counter: dict, *, pretty: bool = False) -> Any:
        return self._call("create", json={"counter": counter}, pretty=pretty)

    def edit(self, counter_id: int, counter: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            json={"counter": counter},
            pretty=pretty,
        )

    def delete(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("delete", counterId=counter_id, pretty=pretty)
