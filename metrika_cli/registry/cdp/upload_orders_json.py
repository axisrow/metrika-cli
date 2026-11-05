"""Загрузка заказов (JSON)

POST /cdp/api/v1/counter/{counterId}/data/orders/json

Подтверждено официальным openapi
(management/openapi/schema/uploadOrdersJson_1.md, ревизия r21770580).
Тело {"orders": [...]}, merge_mode — обязательный query-параметр.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "upload_orders_json",
    "POST",
    "cdp/api/v1/counter/{counterId}/data/orders/json",
    "Загрузка заказов (JSON)",
    path_params=("counterId",),
)
