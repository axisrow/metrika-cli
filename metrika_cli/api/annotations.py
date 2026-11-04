"""Ресурс «Примечания на графиках» (Management API) — 5 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
Пути и методы сверены с живым OpenAPI-справочником
(https://yandex.ru/dev/metrika/ru/management/openapi/chart_annotation/,
проверено 2026-11-04): findAll (list, GET), create (POST), get (GET),
update (edit, PUT), delete (DELETE).
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_ANNOTATIONS


class Annotations(Resource):
    group = GROUP_ANNOTATIONS

    def list(self, counter_id: int, *, pretty: bool = False) -> Any:
        return self._call("list", counterId=counter_id, pretty=pretty)

    def create(self, counter_id: int, annotation: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "create",
            counterId=counter_id,
            json={"chart_annotation": annotation},
            pretty=pretty,
        )

    def get(self, counter_id: int, annotation_id: int, *, pretty: bool = False) -> Any:
        return self._call("get", counterId=counter_id, id=annotation_id, pretty=pretty)

    def edit(
        self,
        counter_id: int,
        annotation_id: int,
        annotation: dict,
        *,
        pretty: bool = False,
    ) -> Any:
        return self._call(
            "edit",
            counterId=counter_id,
            id=annotation_id,
            json={"chart_annotation": annotation},
            pretty=pretty,
        )

    def delete(
        self, counter_id: int, annotation_id: int, *, pretty: bool = False
    ) -> Any:
        return self._call(
            "delete", counterId=counter_id, id=annotation_id, pretty=pretty
        )
