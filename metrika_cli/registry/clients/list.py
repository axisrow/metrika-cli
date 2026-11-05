"""Список клиентов Яндекс Директа

GET /management/v1/clients

Подтверждено официальным openapi (management/openapi/clients/getClients.md,
ревизия r21770580): ``counters`` — ОБЯЗАТЕЛЬНЫЙ query-параметр,
ID счётчиков через запятую; ответ {"clients": [{id, chief_login, ...}]}.
"""

from .._core import Endpoint, GROUP_CLIENTS

ENDPOINT = Endpoint(
    GROUP_CLIENTS,
    "list",
    "GET",
    "management/v1/clients",
    "Список клиентов Директа",
)
