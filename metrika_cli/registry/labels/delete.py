"""Удалить метку

DELETE /management/v1/label/{labelId}
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "delete",
    "DELETE",
    "management/v1/label/{labelId}",
    "Удалить метку",
    path_params=("labelId",),
)
