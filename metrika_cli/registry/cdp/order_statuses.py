"""Сопоставленные статусы заказов (CDP/CRM)

GET /cdp/api/v1/counter/{counterId}/schema/order_statuses

Подтверждено официальным openapi
(management/openapi/schema/getOrderStatuses.md, ревизия r21770580).
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "order_statuses",
    "GET",
    "cdp/api/v1/counter/{counterId}/schema/order_statuses",
    "Сопоставленные статусы заказов",
    path_params=("counterId",),
)
