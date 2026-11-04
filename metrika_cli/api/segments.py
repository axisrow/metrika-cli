"""Ресурс «Сегменты счётчика» (Management API, apisegment) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_SEGMENTS


class Segments(Resource):
    group = GROUP_SEGMENTS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def create(self, counter_id: int, segment: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create",
            counterId=counter_id,
            json={"segment": segment},
            pretty=pretty,
        )

    def get(self, counter_id: int, segment_id: str, *, pretty: bool = False) -> Any:
        return self._call(
            "get", counterId=counter_id, segmentId=segment_id, pretty=pretty
        )

    def edit(
        self, counter_id: int, segment_id: str, segment: dict, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            segmentId=segment_id,
            json={"segment": segment},
            pretty=pretty,
        )

    def delete(self, counter_id: int, segment_id: str, *, pretty: bool = False) -> Any:
        return self._call(
            "delete", counterId=counter_id, segmentId=segment_id, pretty=pretty
        )
