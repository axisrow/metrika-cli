"""Ресурс «Офлайн-звонки» (Data Import, management-хост) — 3 эндпоинта.

Требуемый scope токена: ``metrika:offline_data``. Формат CSV — гайд
«Передача данных о звонках»: https://yandex.ru/dev/metrika/ru/management/calls.md
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_CALLS


class Calls(Resource):
    group = GROUP_CALLS

    def upload(
        self,
        counter_id: int,
        file_path: str,
        *,
        client_id_type: str,
        comment: Optional[str] = None,
        new_goal_name: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить CSV-файл со звонками (multipart, поле ``file``)."""
        params = {
            k: v
            for k, v in (
                ("client_id_type", client_id_type),
                ("comment", comment),
                ("new_goal_name", new_goal_name),
            )
            if v is not None
        }
        return self._upload(
            "upload",
            file_path,
            params=params,
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
        """Список загрузок звонков счётчика."""
        params = {
            k: v for k, v in (("limit", limit), ("offset", offset)) if v is not None
        }
        return self._call(
            "uploadings", counterId=counter_id, params=params or None, pretty=pretty
        )

    def uploading(
        self,
        counter_id: int,
        id: int,
        *,
        pretty: bool = False,
    ) -> Any:
        """Информация о загрузке звонков по ID."""
        return self._call("uploading", counterId=counter_id, id=id, pretty=pretty)
