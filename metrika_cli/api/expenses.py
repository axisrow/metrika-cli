"""Ресурс «Расходы на рекламу» (Data Import, management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ..base import Resource
from ..registry import GROUP_EXPENSES

#: Multipart-тип загружаемого CSV-файла.
CSV_MIME = "text/csv"


def _csv_file(filename: str, content: bytes) -> Dict[str, Any]:
    """Multipart-поле ``file`` для загрузки CSV."""
    return {"file": (filename, content, CSV_MIME)}


def _optional(**kwargs: Any) -> Dict[str, Any]:
    """Отобрать только переданные (не None) query-параметры."""
    return {k: v for k, v in kwargs.items() if v is not None}


class Expenses(Resource):
    group = GROUP_EXPENSES

    def upload(
        self,
        counter_id: int,
        filename: str,
        content: bytes,
        *,
        comment: Optional[str] = None,
        provider: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить CSV с расходами (multipart/form-data)."""
        return self._call(
            "upload",
            params=_optional(comment=comment, provider=provider),
            files=_csv_file(filename, content),
            pretty=pretty,
            counterId=counter_id,
        )

    def delete(
        self,
        counter_id: int,
        filename: str,
        content: bytes,
        *,
        comment: Optional[str] = None,
        provider: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Удалить расходы по CSV-файлу условий (multipart/form-data)."""
        return self._call(
            "delete",
            params=_optional(comment=comment, provider=provider),
            files=_csv_file(filename, content),
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
        return self._call(
            "delete_single",
            params=_optional(
                date=date,
                trafficSource=traffic_source,
                trafficSourceDetail=traffic_source_detail,
                UTMSource=utm_source,
                UTMMedium=utm_medium,
                UTMCampaign=utm_campaign,
                UTMTerm=utm_term,
                UTMContent=utm_content,
                provider=provider,
                comment=comment,
            ),
            pretty=pretty,
            counterId=counter_id,
        )

    def list(
        self,
        counter_id: int,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        pretty: bool = False,
    ) -> Any:
        """Список загрузок расходов."""
        return self._call(
            "list",
            params=_optional(limit=limit, offset=offset),
            pretty=pretty,
            counterId=counter_id,
        )

    def get(
        self,
        counter_id: int,
        uploading_id: int,
        *,
        pretty: bool = False,
    ) -> Any:
        """Информация о загрузке расходов."""
        return self._call(
            "get",
            pretty=pretty,
            counterId=counter_id,
            uploadingId=uploading_id,
        )
