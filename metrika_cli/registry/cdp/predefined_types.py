"""Типы пользовательских атрибутов (CDP/CRM)

GET /cdp/api/v1/counter/{counterId}/schema/predefined_types

Подтверждено официальным openapi
(management/openapi/schema/getPredefinedTypes.md, ревизия r21770580).
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "predefined_types",
    "GET",
    "cdp/api/v1/counter/{counterId}/schema/predefined_types",
    "Типы пользовательских атрибутов",
    path_params=("counterId",),
)
