"""Создать лог-запрос

POST /management/v1/counter/{counterId}/logrequests

Параметры — в query-строке: date1, date2, fields, source (обязательные),
attribution (необязательный). Тела у запроса нет.
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/logrequests",
    "Создать лог-запрос (query: date1, date2, fields, source [, attribution])",
    path_params=("counterId",),
)
