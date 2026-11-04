"""Список меток пользователя

GET /management/v1/labels
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "list",
    "GET",
    "management/v1/labels",
    "Список меток пользователя",
)
