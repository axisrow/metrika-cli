"""Последние загрузки (CDP/CRM)

GET /cdp/api/v1/counter/{counterId}/last_uploadings

Подтверждено официальным openapi
(management/openapi/schema/getLastUploadings.md, ревизия r21770580).
Query: datetime_offset, limit (1..1000), source.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "last_uploadings",
    "GET",
    "cdp/api/v1/counter/{counterId}/last_uploadings",
    "Последние загрузки CDP/CRM",
    path_params=("counterId",),
)
