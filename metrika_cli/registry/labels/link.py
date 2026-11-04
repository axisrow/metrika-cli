"""Привязать счётчик к метке

POST /management/v1/counter/{counterId}/label/{labelId}

Тела запроса нет — связь задаётся только параметрами пути
(openapi: counter-label/setCounterLabel).
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "link",
    "POST",
    "management/v1/counter/{counterId}/label/{labelId}",
    "Привязать счётчик к метке",
    path_params=("counterId", "labelId"),
)
