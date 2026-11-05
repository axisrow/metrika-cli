"""Загрузка заказов (CSV)

POST /cdp/api/v1/counter/{counterId}/data/orders/csv

Подтверждено официальным openapi
(management/openapi/schema/uploadOrders.md, ревизия r21770580).
Multipart-файл (поле file) + query: columns_mapping (обязательный),
merge_mode (обязательный), delimiter_type.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "upload_orders",
    "POST",
    "cdp/api/v1/counter/{counterId}/data/orders/csv",
    "Загрузка заказов (CSV)",
    multipart=True,
    path_params=("counterId",),
)
