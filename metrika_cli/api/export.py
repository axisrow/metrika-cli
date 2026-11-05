"""Ресурс «Экспорт в Yandex Cloud» (/export/v1) — 2 эндпоинта.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_EXPORT


class CloudExport(Resource):
    group = GROUP_EXPORT

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        """Объекты счётчика, экспортируемые в Yandex Cloud."""
        return self._call("list", counterId=counter_id, pretty=pretty)

    def delete(self, ce_id: int, counter_id: int, *, pretty: bool = False) -> Any:
        """Отключить экспорт: ce_id — ID экспорта (из list), counter_id — счётчик."""
        return self._call(
            "delete", ceId=ce_id, counterId=counter_id, pretty=pretty
        )
