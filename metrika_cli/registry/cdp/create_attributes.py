"""Создание атрибутов (CDP/CRM)

POST /cdp/api/v1/counter/{counterId}/schema/attributes

Подтверждено официальным openapi
(management/openapi/schema/createAttributes.md, ревизия r21770580).
``entity_type`` — обязательный query-параметр; тело {"attributes": [...]}.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "create_attributes",
    "POST",
    "cdp/api/v1/counter/{counterId}/schema/attributes",
    "Создать атрибуты",
    path_params=("counterId",),
)
