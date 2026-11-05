"""Ресурс «Клиенты Директа» (Management API) — 1 эндпоинт.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_CLIENTS


class Clients(Resource):
    group = GROUP_CLIENTS

    def list(self, counter_ids: str, *, pretty: bool = False) -> Any:
        """Список клиентов Директа.

        ``counters`` — обязательный query-параметр API: ID счётчиков
        через запятую.
        """
        return self._call(
            "list", params={"counters": counter_ids}, pretty=pretty
        )
