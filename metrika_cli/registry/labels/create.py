"""Создать метку

POST /management/v1/labels
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "create",
    "POST",
    "management/v1/labels",
    'Создать метку (тело: {"label": {...}})',
)
