"""Загрузка параметров посетителей

POST /management/v1/counter/{counterId}/user_params/uploadings/upload
"""

from .._core import Endpoint, GROUP_USER_PARAMS

ENDPOINT = Endpoint(
    GROUP_USER_PARAMS,
    "upload",
    "POST",
    "management/v1/counter/{counterId}/user_params/uploadings/upload",
    "Загрузить CSV-файл с параметрами посетителей",
    multipart=True,
    path_params=("counterId",),
)

# Query-параметры (openapi user_params/upload, проверено 2026-11-05):
#   action — ОБЯЗАТЕЛЬНЫЙ, тип действия:
#     update — добавление параметров; delete_keys — удаление параметров.
# Multipart-тело: form-поле ``file`` (CSV с параметрами).
