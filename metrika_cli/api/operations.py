"""Ресурс «Операции» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_OPERATIONS


class Operations(Resource):
    group = GROUP_OPERATIONS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def get(self, counter_id: int, operation_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "get",
            counterId=counter_id,
            operationId=operation_id,
            pretty=pretty,
        )

    def create(self, counter_id: int, operation: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create",
            counterId=counter_id,
            json={"operation": operation},
            pretty=pretty,
        )

    def edit(
        self,
        counter_id: int,
        operation_id: int,
        operation: dict,
        *,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            operationId=operation_id,
            json={"operation": operation},
            pretty=pretty,
        )

    def delete(
        self, counter_id: int, operation_id: int, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "delete",
            counterId=counter_id,
            operationId=operation_id,
            pretty=pretty,
        )
