"""Отключение экспорта на счётчике

DELETE /export/v1/cloud/{ceId}/counter/{counterId}

Подтверждено официальным openapi
(management/openapi/cloud/removeCounter.md, ревизия r21770580):
``ceId`` — идентификатор экспорта в Yandex Cloud (из list),
``counterId`` — счётчик.
"""

from .._core import Endpoint, GROUP_EXPORT

ENDPOINT = Endpoint(
    GROUP_EXPORT,
    "delete",
    "DELETE",
    "export/v1/cloud/{ceId}/counter/{counterId}",
    "Отключить экспорт счётчика в Yandex Cloud",
    path_params=("ceId", "counterId"),
)
