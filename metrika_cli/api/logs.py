"""Ресурс «Лог-запросы» (Logs API) — 7 эндпоинтов.

Асинхронный workflow: evaluate → create → poll(info) → download_part,
cancel (необработанный) / clean (обработанный). Ограничения: период ≤1 год,
fields ≤3000 символов, 10 ГБ на счётчик.
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_LOGS


class Logs(Resource):
    group = GROUP_LOGS

    def evaluate(
        self,
        counter_id: int,
        *,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        source: Optional[str] = None,
        fields: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        params = {
            k: v
            for k, v in (
                ("date1", date1),
                ("date2", date2),
                ("source", source),
                ("fields", fields),
            )
            if v is not None
        }
        return self._call("evaluate", counterId=counter_id, params=params or None)

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def create(self, counter_id: int, body: dict, *, pretty: bool = False) -> Any:
        return self._call("create", counterId=counter_id, json=body, pretty=pretty)

    def info(self, counter_id: int, request_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "info", counterId=counter_id, requestId=request_id, pretty=pretty
        )

    def cancel(self, counter_id: int, request_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "cancel", counterId=counter_id, requestId=request_id, pretty=pretty
        )

    def clean(self, counter_id: int, request_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "clean", counterId=counter_id, requestId=request_id, pretty=pretty
        )

    def download_part(self, counter_id: int, request_id: int, part_number: int) -> Any:
        """CSV-часть выгрузки: вернуть текст (для --out или stdout)."""
        return self._call(
            "download_part",
            counterId=counter_id,
            requestId=request_id,
            partNumber=part_number,
            raw=True,
        )
