"""Все атрибуты сущностей (CDP/CRM)

GET /cdp/api/v1/counter/{counterId}/schema/attributes

Подтверждено официальным openapi
(management/openapi/schema/getAttributes.md, ревизия r21770580).
``entity_type`` — ОБЯЗАТЕЛЬНЫЙ query-параметр: CONTACT | COMPANY |
ORDER | SIMPLE_ORDER.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "attributes",
    "GET",
    "cdp/api/v1/counter/{counterId}/schema/attributes",
    "Все атрибуты сущностей",
    path_params=("counterId",),
)
