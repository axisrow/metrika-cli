"""Ресурс «Офлайн-конверсии» (Data Import, management-хост) — 3 эндпоинта.

Требуемый scope токена: ``metrika:offline_data``. Confirm/delete в текущем
openapi offline_conversions отсутствуют (проверено 2026-11-04) — не
реализованы намеренно.
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_CONVERSIONS


class Conversions(Resource):
    group = GROUP_CONVERSIONS

    def upload(
        self,
        counter_id: int,
        file_path: str,
        *,
        comment: Optional[str] = None,
        type_: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить CSV-файл с конверсиями (multipart, поле ``file``)."""
        params = {
            k: v for k, v in (("comment", comment), ("type", type_)) if v is not None
        }
        return self._upload(
            "upload",
            file_path,
            params=params or None,
            pretty=pretty,
            counterId=counter_id,
        )

    def uploadings(
        self,
        counter_id: int,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type_: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Список загрузок конверсий счётчика."""
        params = {
            k: v
            for k, v in (("limit", limit), ("offset", offset), ("type", type_))
            if v is not None
        }
        return self._call(
            "uploadings", counterId=counter_id, params=params or None, pretty=pretty
        )

    def uploading(
        self,
        counter_id: int,
        id: int,
        *,
        type_: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Информация о загрузке по ID."""
        params = {"type": type_} if type_ is not None else None
        return self._call(
            "uploading", counterId=counter_id, id=id, params=params, pretty=pretty
        )
