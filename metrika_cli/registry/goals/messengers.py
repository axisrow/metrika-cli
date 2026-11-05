"""Список мессенджеров (справочник для целей-чатов)

GET /management/v1/messengers

Подтверждено официальным openapi (management/openapi/goal/getMessengers.md,
ревизия r21770580). Параметров нет; ответ {"messengers": [...]}.
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "messengers",
    "GET",
    "management/v1/messengers",
    "Справочник мессенджеров",
)
