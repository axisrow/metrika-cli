"""Ресурс «CDP/CRM: клиенты и заказы» (/cdp/api/v1) — загрузки и schema.

Параметры сверены с официальным openapi
(management/openapi/schema/*.md, ревизия r21770580, 2026-11-05):
- CSV-загрузки — multipart (поле ``file``) + query columns_mapping,
  merge_mode (обязательные), delimiter_type (опциональный);
- JSON-загрузки — тело {"contacts": [...]} / {"orders": [...]},
  merge_mode (обязательный);
- last_uploadings — query datetime_offset, limit (1..1000), source;
- schema: entity_type (CONTACT|ORDER) обязателен у attributes
  (GET/POST), тела POST — {"attributes": [...]} / {"order_statuses":
  [...]} / {"attributes": [...], "items": [...]}.
"""

from __future__ import annotations

from typing import Any, Optional

from ..base import Resource
from ..registry import GROUP_CDP


class Cdp(Resource):
    group = GROUP_CDP

    def upload_contacts(
        self,
        counter_id: int,
        file_path: str,
        *,
        columns_mapping: str,
        merge_mode: str,
        delimiter_type: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить клиентов из CSV (multipart, поле ``file``)."""
        params = self._csv_params(columns_mapping, merge_mode, delimiter_type)
        return self._upload(
            "upload_contacts", file_path, params=params, pretty=pretty,
            counterId=counter_id,
        )

    def upload_contacts_json(
        self, counter_id: int, contacts: dict, *, merge_mode: str, pretty: bool = False
    ) -> Any:
        """Загрузить клиентов (тело {"contacts": [...]})."""
        return self._call(
            "upload_contacts_json",
            counterId=counter_id,
            params={"merge_mode": merge_mode},
            json=contacts,
            pretty=pretty,
        )

    def upload_orders(
        self,
        counter_id: int,
        file_path: str,
        *,
        columns_mapping: str,
        merge_mode: str,
        delimiter_type: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Загрузить заказы из CSV (multipart, поле ``file``)."""
        params = self._csv_params(columns_mapping, merge_mode, delimiter_type)
        return self._upload(
            "upload_orders", file_path, params=params, pretty=pretty,
            counterId=counter_id,
        )

    def upload_orders_json(
        self, counter_id: int, orders: dict, *, merge_mode: str, pretty: bool = False
    ) -> Any:
        """Загрузить заказы (тело {"orders": [...]})."""
        return self._call(
            "upload_orders_json",
            counterId=counter_id,
            params={"merge_mode": merge_mode},
            json=orders,
            pretty=pretty,
        )

    def upload_simple_orders(
        self,
        counter_id: int,
        file_path: str,
        *,
        merge_mode: str,
        delimiter_type: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Упрощённая загрузка клиентов и заказов (multipart, поле ``file``)."""
        params = self._csv_params(None, merge_mode, delimiter_type)
        return self._upload(
            "upload_simple_orders", file_path, params=params, pretty=pretty,
            counterId=counter_id,
        )

    def last_uploadings(
        self,
        counter_id: int,
        *,
        datetime_offset: Optional[str] = None,
        limit: Optional[int] = None,
        source: Optional[str] = None,
        pretty: bool = False,
    ) -> Any:
        """Последние загрузки CDP/CRM."""
        params = {
            k: v
            for k, v in (
                ("datetime_offset", datetime_offset),
                ("limit", limit),
                ("source", source),
            )
            if v is not None
        }
        return self._call(
            "last_uploadings", counterId=counter_id, params=params or None,
            pretty=pretty,
        )

    # -- schema ----------------------------------------------------------------

    def attributes(self, counter_id: int, entity_type: str, *, pretty: bool = False) -> Any:
        """Все атрибуты сущности (entity_type: CONTACT | ORDER — обязательный)."""
        return self._call(
            "attributes",
            counterId=counter_id,
            params={"entity_type": entity_type},
            pretty=pretty,
        )

    def create_attributes(
        self, counter_id: int, attributes: dict, *, entity_type: str, pretty: bool = False
    ) -> Any:
        """Создать атрибуты (тело {"attributes": [...]}, entity_type обязательный)."""
        return self._call(
            "create_attributes",
            counterId=counter_id,
            params={"entity_type": entity_type},
            json=attributes,
            pretty=pretty,
        )

    def order_statuses(self, counter_id: int, *, pretty: bool = False) -> Any:
        """Сопоставленные статусы заказов."""
        return self._call("order_statuses", counterId=counter_id, pretty=pretty)

    def map_order_statuses(
        self, counter_id: int, order_statuses: dict, *, pretty: bool = False
    ) -> Any:
        """Сопоставить статусы заказов (тело {"order_statuses": [...]})."""
        return self._call(
            "map_order_statuses",
            counterId=counter_id,
            json=order_statuses,
            pretty=pretty,
        )

    def predefined_types(self, counter_id: int, *, pretty: bool = False) -> Any:
        """Типы пользовательских атрибутов."""
        return self._call("predefined_types", counterId=counter_id, pretty=pretty)

    def types(self, counter_id: int, *, pretty: bool = False) -> Any:
        """Типы системных атрибутов."""
        return self._call("types", counterId=counter_id, pretty=pretty)

    def create_products(
        self, counter_id: int, products: dict, *, pretty: bool = False
    ) -> Any:
        """Создать список товаров (тело {"attributes": [...], "items": [...]})."""
        return self._call(
            "create_products", counterId=counter_id, json=products, pretty=pretty
        )

    @staticmethod
    def _csv_params(
        columns_mapping: Optional[str], merge_mode: str, delimiter_type: Optional[str]
    ) -> dict:
        params: dict = {"merge_mode": merge_mode}
        if columns_mapping:
            params["columns_mapping"] = columns_mapping
        if delimiter_type:
            params["delimiter_type"] = delimiter_type
        return params
