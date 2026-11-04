"""Подтверждение загрузки параметров

POST /management/v1/counter/{counterId}/user_params/uploading/{uploadingId}/confirm
"""

from .._core import Endpoint, GROUP_USER_PARAMS

ENDPOINT = Endpoint(
    GROUP_USER_PARAMS,
    "confirm",
    "POST",
    "management/v1/counter/{counterId}/user_params/uploading/{uploadingId}/confirm",
    "Подтвердить загрузку параметров по ID",
    path_params=("counterId", "uploadingId"),
)

# Тело (openapi user_params/confirm): JSON {"uploading": {...}} — в спеке
# помечено required; передаём опционально (см. api.user_params.confirm).
