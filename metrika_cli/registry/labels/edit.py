"""Изменить метку

PUT /management/v1/label/{labelId}
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "edit",
    "PUT",
    "management/v1/label/{labelId}",
    'Изменить метку (тело: {"label": {...}})',
    path_params=("labelId",),
)
