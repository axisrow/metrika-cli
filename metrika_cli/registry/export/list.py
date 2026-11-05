"""Объекты, экспортируемые в Yandex Cloud

GET /export/v1/cloud/counter/{counterId}

Подтверждено официальным openapi
(management/openapi/cloud/getExportsByCounter.md, ревизия r21770580).
ВНИМАНИЕ: префикс НЕ management — раздел экспорта живёт на /export/v1.
"""

from .._core import Endpoint, GROUP_EXPORT

ENDPOINT = Endpoint(
    GROUP_EXPORT,
    "list",
    "GET",
    "export/v1/cloud/counter/{counterId}",
    "Объекты, экспортируемые в Yandex Cloud",
    path_params=("counterId",),
)
