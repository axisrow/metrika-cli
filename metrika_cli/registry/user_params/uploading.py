"""Информация о загрузке параметров

GET /management/v1/counter/{counterId}/user_params/uploading/{uploadingId}
"""

from .._core import Endpoint, GROUP_USER_PARAMS

ENDPOINT = Endpoint(
    GROUP_USER_PARAMS,
    "uploading",
    "GET",
    "management/v1/counter/{counterId}/user_params/uploading/{uploadingId}",
    "Информация о загрузке параметров по ID",
    path_params=("counterId", "uploadingId"),
)

# В вендорном маппинге tapi (2022) у ресурса есть ещё PUT — в текущем
# openapi (проверено 2026-11-05) не задокументирован, не реализован.
