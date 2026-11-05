"""Упрощённая загрузка клиентов и заказов (CSV)

POST /cdp/api/v1/counter/{counterId}/data/simple_orders

Подтверждено официальным openapi
(management/openapi/schema/uploadSimpleOrders.md, ревизия r21770580).
Multipart-файл (поле file) + query: merge_mode (обязательный),
delimiter_type.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "upload_simple_orders",
    "POST",
    "cdp/api/v1/counter/{counterId}/data/simple_orders",
    "Упрощённая загрузка клиентов и заказов (CSV)",
    multipart=True,
    path_params=("counterId",),
)
