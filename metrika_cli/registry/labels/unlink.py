"""Отвязать счётчик от метки

DELETE /management/v1/counter/{counterId}/label/{labelId}
"""

from .._core import Endpoint, GROUP_LABELS

ENDPOINT = Endpoint(
    GROUP_LABELS,
    "unlink",
    "DELETE",
    "management/v1/counter/{counterId}/label/{labelId}",
    "Отвязать счётчик от метки",
    path_params=("counterId", "labelId"),
)
