"""Типы системных атрибутов (CDP/CRM)

GET /cdp/api/v1/counter/{counterId}/schema/types

Подтверждено официальным openapi
(management/openapi/schema/getTypes.md, ревизия r21770580).
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "types",
    "GET",
    "cdp/api/v1/counter/{counterId}/schema/types",
    "Типы системных атрибутов",
    path_params=("counterId",),
)
