"""Ресурс «Отчёты» (Reports API, /stat/v1) — 6 эндпоинтов.

Общие параметры: ids, metrics (≤20), dimensions (≤10), date1/date2,
filters, sort, limit (≤100000, default 100), offset (с 1), preset, lang;
параметры семплирования/окружения: accuracy, proposed_accuracy, timezone
(±hh:mm), include_undefined, direct_client_logins (проверено по openapi
stat 2026-11-05). Формат ответа: JSON или CSV (расширение .csv в пути).
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_STAT


class Stat(Resource):
    group = GROUP_STAT

    # -- table ---------------------------------------------------------------
    def table(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: Optional[str] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        filters: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "table",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )

    # -- bytime --------------------------------------------------------------
    def bytime(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: Optional[str] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        group: Optional[str] = None,
        filters: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        top_keys: Optional[str] = None,
        row_ids: Optional[str] = None,
        include_annotations: Optional[bool] = None,
        annotation_groups: Optional[str] = None,
        keys_sort: Optional[str] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "bytime",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )

    # -- comparison ----------------------------------------------------------
    def comparison(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: Optional[str] = None,
        date1_a: Optional[str] = None,
        date2_a: Optional[str] = None,
        date1_b: Optional[str] = None,
        date2_b: Optional[str] = None,
        filters_a: Optional[str] = None,
        filters_b: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "comparison",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )

    # -- drilldown -----------------------------------------------------------
    def drilldown(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: str,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        parent_id: Optional[str] = None,
        filters: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        only_expandable_undefined: Optional[bool] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "drilldown",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )

    # -- comparison_drilldown --------------------------------------------------
    def comparison_drilldown(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: Optional[str] = None,
        date1_a: Optional[str] = None,
        date2_a: Optional[str] = None,
        date1_b: Optional[str] = None,
        date2_b: Optional[str] = None,
        filters_a: Optional[str] = None,
        filters_b: Optional[str] = None,
        parent_id: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        only_expandable_undefined: Optional[bool] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "comparison_drilldown",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )

    # -- pivot ---------------------------------------------------------------
    def pivot(
        self,
        *,
        ids: str,
        metrics: str,
        dimensions: str,
        pivot_dimensions: str,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        filters: Optional[str] = None,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        preset: Optional[str] = None,
        lang: Optional[str] = None,
        accuracy: Optional[str] = None,
        proposed_accuracy: Optional[bool] = None,
        timezone: Optional[str] = None,
        include_undefined: Optional[bool] = None,
        direct_client_logins: Optional[str] = None,
        pivot_limit: Optional[int] = None,
        pivot_offset: Optional[int] = None,
        csv: bool = False,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "pivot",
            params=_clean(locals(), "self", "csv", "pretty"),
            path_suffix=".csv" if csv else "",
            raw=csv,
            pretty=pretty,
        )


def _clean(locals_: dict, *skip: str) -> dict:
    """Оставить только явно переданные query-параметры."""
    return {
        k: v
        for k, v in locals_.items()
        if k not in skip and not k.startswith("_") and v is not None
    }
