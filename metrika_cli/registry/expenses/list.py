"""Список загрузок расходов

GET /management/v1/counter/{counterId}/expense/uploadings

Query: limit (по умолчанию 10000), offset (по умолчанию 0).
Ответ: {"uploadings": [...]}.
"""

from .._core import Endpoint, GROUP_EXPENSES

ENDPOINT = Endpoint(
    GROUP_EXPENSES,
    "list",
    "GET",
    "management/v1/counter/{counterId}/expense/uploadings",
    "Список загрузок расходов",
    path_params=("counterId",),
)
