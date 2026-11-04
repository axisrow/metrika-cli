"""Ресурс «Счётчики» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_COUNTERS


class Counters(Resource):
    group = GROUP_COUNTERS

    def list(self, *, pretty: bool = False) -> Any:
        return self._call("list", pretty=pretty)

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
