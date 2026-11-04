"""Информация о метке

GET /management/v1/label/{labelId}
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "get",
    "GET",
    "management/v1/label/{labelId}",
    "Информация о метке",
    path_params=("labelId",),
)
