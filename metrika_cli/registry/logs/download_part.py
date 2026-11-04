"""Скачать часть выгрузки (CSV)

GET /management/v1/counter/{counterId}/logrequest/{requestId}/part/{partNumber}/download
"""

from .._core import Endpoint, GROUP_LOGS

ENDPOINT = Endpoint(
    GROUP_LOGS,
    "download_part",
    "GET",
    "management/v1/counter/{counterId}/logrequest/{requestId}/part/{partNumber}/download",
    "Скачать часть выгрузки (CSV)",
    path_params=("counterId", "requestId", "partNumber"),
)
