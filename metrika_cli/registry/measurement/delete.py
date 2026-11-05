"""Удаление токена Measurement Protocol

POST /management/v1/counter/{counterId}/measurement/delete

Подтверждено официальным openapi
(management/openapi/measurement/deleteToken.md, ревизия r21770580):
``token`` — ОБЯЗАТЕЛЬНЫЙ query-параметр.
"""

from .._core import Endpoint, GROUP_MEASUREMENT

ENDPOINT = Endpoint(
    GROUP_MEASUREMENT,
    "delete",
    "POST",
    "management/v1/counter/{counterId}/measurement/delete",
    "Удалить токен Measurement Protocol",
    path_params=("counterId",),
)
