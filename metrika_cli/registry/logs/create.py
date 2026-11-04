"""Создать лог-запрос

POST /management/v1/counter/{counterId}/logrequests

Тело: {source, date1, date2, fields}; период ≤1 год; статус created.
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "create",
    "POST",
    "management/v1/counter/{counterId}/logrequests",
    "Создать лог-запрос (тело: {\"source\",\"date1\",\"date2\",\"fields\"})",
    path_params=("counterId",),
)
