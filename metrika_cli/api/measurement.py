"""Ресурс «Measurement Protocol» (Management API) — 2 эндпоинта.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_MEASUREMENT


class Measurement(Resource):
    group = GROUP_MEASUREMENT

    def generate(self, counter_id: int, *, pretty: bool = False) -> Any:
        """Сгенерировать токен Measurement Protocol (ответ — строка)."""
        return self._call("generate", counterId=counter_id, pretty=pretty)

    def delete(self, counter_id: int, token: str, *, pretty: bool = False) -> Any:
        """Удалить токен Measurement Protocol (token — query-параметр API)."""
        return self._call(
            "delete", counterId=counter_id, params={"token": token}, pretty=pretty
        )
