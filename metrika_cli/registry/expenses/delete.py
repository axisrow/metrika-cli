"""Удаление данных о расходах как multipart/form-data

POST /management/v1/counter/{counterId}/expense/delete

Multipart-поле ``file``: CSV с условиями удаления (обязательная колонка
Date). Query: comment, provider. Ответ: {"uploading": {...}}.
"""

from .._core import Endpoint, GROUP_EXPENSES

ENDPOINT = Endpoint(
    GROUP_EXPENSES,
    "delete",
    "POST",
    "management/v1/counter/{counterId}/expense/delete",
    "Удаление расходов по CSV-условиям (multipart)",
    multipart=True,
    path_params=("counterId",),
)
