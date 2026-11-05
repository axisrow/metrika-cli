"""Сопоставление статусов заказов (CDP/CRM)

POST /cdp/api/v1/counter/{counterId}/schema/order_statuses

Подтверждено официальным openapi
(management/openapi/schema/mapOrderStatuses.md, ревизия r21770580).
Тело {"order_statuses": [{id, humanized, type, goal_action_ids}]}.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "map_order_statuses",
    "POST",
    "cdp/api/v1/counter/{counterId}/schema/order_statuses",
    "Сопоставить статусы заказов",
    path_params=("counterId",),
)
