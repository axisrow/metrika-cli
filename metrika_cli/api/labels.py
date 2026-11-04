"""Ресурс «Метки» (Management API) — 7 эндпоинтов.

Имена методов совпадают с ``op`` соответствующих эндпоинтов в registry.
Пути подтверждены живым openapi-справочником Management API
(label/{getLabels,createLabel,getLabel,updateLabel,deleteLabel},
counter-label/{setCounterLabel,unsetCounterLabel}; сверено 2026-11-04).
"""

from __future__ import annotations

from typing import Any

from ..base import Resource
from ..registry import GROUP_LABELS


class Labels(Resource):
    group = GROUP_LABELS

    def list(self, *, pretty: bool = False) -> Any:
        return self._call("list", pretty=pretty)

    def get(self, label_id: int, *, pretty: bool = False) -> Any:
        return self._call("get", labelId=label_id, pretty=pretty)

    def create(self, label: dict, *, pretty: bool = False) -> Any:
        return self._call("create", json={"label": label}, pretty=pretty)

    def edit(self, label_id: int, label: dict, *, pretty: bool = False) -> Any:
        return self._call(
            "edit",
            labelId=label_id,
            json={"label": label},
            pretty=pretty,
        )

    def delete(self, label_id: int, *, pretty: bool = False) -> Any:
        return self._call("delete", labelId=label_id, pretty=pretty)

    def link(self, counter_id: int, label_id: int, *, pretty: bool = False) -> Any:
        return self._call("link", counterId=counter_id, labelId=label_id, pretty=pretty)

    def unlink(self, counter_id: int, label_id: int, *, pretty: bool = False) -> Any:
        return self._call(
            "unlink", counterId=counter_id, labelId=label_id, pretty=pretty
        )
