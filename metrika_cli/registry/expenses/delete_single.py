"""Удаление данных о расходах в запросе

POST /management/v1/counter/{counterId}/expense/delete_single

Условия удаления передаются в query: date (обязателен), trafficSource,
trafficSourceDetail, UTM-метки (регистрозависимые), provider, comment.
Ответ: {"uploading": {...}}.
"""

from .._core import Endpoint, GROUP_EXPENSES

ENDPOINT = Endpoint(
    GROUP_EXPENSES,
    "delete_single",
    "POST",
    "management/v1/counter/{counterId}/expense/delete_single",
    "Удаление расходов по условиям в запросе (date обязателен)",
    path_params=("counterId",),
)
