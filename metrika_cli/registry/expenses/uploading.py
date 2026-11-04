"""Информация о загрузке расходов

GET /management/v1/counter/{counterId}/expense/uploading/{uploadingId}

Ответ: {"uploading": {...}}.
"""

from .._core import Endpoint, GROUP_EXPENSES

ENDPOINT = Endpoint(
    GROUP_EXPENSES,
    "uploading",
    "GET",
    "management/v1/counter/{counterId}/expense/uploading/{uploadingId}",
    "Информация о загрузке расходов",
    path_params=("counterId", "uploadingId"),
)
