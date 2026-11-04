"""Ресурс «Параметры посетителей» (Data Import, management-хост) — 4 эндпоинта.

Требуемый scope токена: ``metrika:user_params``. Пути и формат сверены с
openapi Management API (страницы user_params/*, проверено 2026-11-05):
multipart-поле ``file``, query ``action`` (``update`` | ``delete_keys``);
DELETE/PUT из вендорного маппинга tapi (2022) в текущем openapi не
задокументированы — не реализованы.
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_USER_PARAMS


class UserParams(Resource):
    group = GROUP_USER_PARAMS

    def upload(
        self,
        counter_id: int,
        file_path: str,
        *,
        action: str = "update",
        pretty: bool = False,
    ) -> Any:
        """Загрузить CSV-файл с параметрами (multipart, поле ``file``).

        ``action``: ``update`` — добавить параметры, ``delete_keys`` — удалить.
        """
        return self._upload(
            "upload",
            file_path,
            params={"action": action},
            pretty=pretty,
            counterId=counter_id,
        )

    def uploadings(
        self,
        counter_id: int,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        pretty: bool = False,
    ) -> Any:
        """Список загрузок параметров счётчика."""
        params = {
            k: v for k, v in (("limit", limit), ("offset", offset)) if v is not None
        }
        return self._call(
            "uploadings", counterId=counter_id, params=params or None, pretty=pretty
        )

    def uploading(
        self, counter_id: int, uploading_id: int, *, pretty: bool = False
    ) -> Any:
        """Информация о загрузке параметров по ID."""
        return self._call(
            "uploading",
            counterId=counter_id,
            uploadingId=uploading_id,
            pretty=pretty,
        )

    def confirm(
        self,
        counter_id: int,
        uploading_id: int,
        *,
        uploading: Optional[dict] = None,
        pretty: bool = False,
    ) -> Any:
        """Подтвердить загрузку параметров.

        ``uploading`` — объект загрузки для тела ``{"uploading": {...}}``;
        в openapi тело помечено required, но фактически POST уходит и без
        него (живой вызов недоступен — формат передаём как в спеке).
        """
        return self._call(
            "confirm",
            counterId=counter_id,
            uploadingId=uploading_id,
            json={"uploading": uploading} if uploading is not None else None,
            pretty=pretty,
        )
