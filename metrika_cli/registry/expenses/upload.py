"""Загрузка расходов как multipart/form-data

POST /management/v1/counter/{counterId}/expense/upload

Multipart-поле ``file``: CSV с обязательными колонками Date,
UTMSource/TrafficSource, Expenses. Query: comment, provider.
Ответ: {"uploading": {...}}.
"""

from .._core import Endpoint, GROUP_EXPENSES

ENDPOINT = Endpoint(
    GROUP_EXPENSES,
    "upload",
    "POST",
    "management/v1/counter/{counterId}/expense/upload",
    "Загрузка расходов (multipart CSV)",
    multipart=True,
    path_params=("counterId",),
)
