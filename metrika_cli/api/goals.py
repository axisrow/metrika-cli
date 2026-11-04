"""Ресурс «Цели» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_GOALS


class Goals(Resource):
    group = GROUP_GOALS

    def list(
        self, counter_id: int, *, use_deleted: bool = False, pretty: bool = False
    ) -> Any:
        return self._call(
            "list",
            counterId=counter_id,
            params={"useDeleted": use_deleted},
            pretty=pretty,
        )

    def get(self, counter_id: int, goal_id: int, *, pretty: bool = False) -> Any:
        return self._call("get", counterId=counter_id, goalId=goal_id, pretty=pretty)

    def create(self, counter_id: int, goal: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create", counterId=counter_id, json={"goal": goal}, pretty=pretty
        )

    def edit(
        self, counter_id: int, goal_id: int, goal: dict, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            goalId=goal_id,
            json={"goal": goal},
            pretty=pretty,
        )

    def delete(self, counter_id: int, goal_id: int, *, pretty: bool = False) -> Any:
        return self._call("delete", counterId=counter_id, goalId=goal_id, pretty=pretty)
