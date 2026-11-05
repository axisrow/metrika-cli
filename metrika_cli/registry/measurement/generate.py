"""Генерация токена Measurement Protocol

GET /management/v1/counter/{counterId}/measurement/generate

Подтверждено официальным openapi
(management/openapi/measurement/generateToken.md, ревизия r21770580).
Ответ — строка-токен.
"""

from .._core import Endpoint, GROUP_MEASUREMENT

ENDPOINT = Endpoint(
    GROUP_MEASUREMENT,
    "generate",
    "GET",
    "management/v1/counter/{counterId}/measurement/generate",
    "Сгенерировать токен Measurement Protocol",
    path_params=("counterId",),
)
