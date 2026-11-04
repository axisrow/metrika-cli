"""Оценить возможность создания лог-запроса

GET /management/v1/counter/{counterId}/logrequests/evaluate

Параметры: date1, date2, source (hits|visits), fields (≤3000 символов).
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "evaluate",
    "GET",
    "management/v1/counter/{counterId}/logrequests/evaluate",
    "Проверить, вернёт ли запрос данные (date1/date2/source/fields)",
    path_params=("counterId",),
)
