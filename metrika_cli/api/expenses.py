"""Ресурс «Расходы на рекламу» (Data Import, management-хост) — 5 эндпоинтов.

Требуемый scope токена: ``metrika:expenses``. Данные Директа загружать не
нужно (Метрика получает их автоматически); confirm в openapi отсутствует,
удаление — через ``delete`` (multipart CSV условий) или ``delete_single``
(условия в query). Проверено по openapi 2026-11-05.
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_EXPENSES


class Expenses(Resource):
    group = GROUP_EXPENSES

    def upload(
        self,
        counter_id: int,
        file_path: str,
        *,
        comment: Optional[str] = None,
        provider: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить CSV с расходами (multipart, поле ``file``)."""
        params = {
            k: v
            for k, v in (("comment", comment), ("provider", provider))
            if v is not None
        }
        return self._upload(
            "upload",
            file_path,
            params=params or None,
            pretty=pretty,
            counterId=counter_id,
        )

    def delete(
        self,
        counter_id: int,
        file_path: str,
        *,
        comment: Optional[str] = None,
        provider: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Удалить расходы по CSV-файлу условий (multipart, поле ``file``)."""
        params = {
            k: v
            for k, v in (("comment", comment), ("provider", provider))
            if v is not None
        }
        return self._upload(
            "delete",
            file_path,
            params=params or None,
            pretty=pretty,
            counterId=counter_id,
        )

    def delete_single(  # noqa: PLR0913 — условия удаления зеркалят query API
        self,
        counter_id: int,
        date: str,
        *,
        traffic_source: Optional[str] = None,
        traffic_source_detail: Optional[str] = None,
        utm_source: Optional[str] = None,
        utm_medium: Optional[str] = None,
        utm_campaign: Optional[str] = None,
        utm_term: Optional[str] = None,
        utm_content: Optional[str] = None,
        provider: Optional[str] = None,
        comment: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Удалить расходы по условиям, переданным в query запроса."""
        pairs = (
            ("date", date),
            ("trafficSource", traffic_source),
            ("trafficSourceDetail", traffic_source_detail),
            ("UTMSource", utm_source),
            ("UTMMedium", utm_medium),
            ("UTMCampaign", utm_campaign),
            ("UTMTerm", utm_term),
            ("UTMContent", utm_content),
            ("provider", provider),
            ("comment", comment),
        )
        params = {k: v for k, v in pairs if v is not None}
        return self._call(
            "delete_single", counterId=counter_id, params=params, pretty=pretty
        )

    def uploadings(
        self,
        counter_id: int,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        pretty: bool = False,
    ) -> Any:
        """Список загрузок расходов счётчика."""
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
        """Информация о загрузке расходов по ID."""
        return self._call(
            "uploading", counterId=counter_id, uploadingId=id, pretty=pretty
        )
