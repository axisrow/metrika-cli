"""Загрузить офлайн-конверсии

POST /management/v1/counter/{counterId}/offline_conversions/upload
"""

from .._core import Endpoint, GROUP_CONVERSIONS

ENDPOINT = Endpoint(
    GROUP_CONVERSIONS,
    "upload",
    "POST",
    "management/v1/counter/{counterId}/offline_conversions/upload",
    "Загрузить CSV-файл с офлайн-конверсиями",
    multipart=True,
    path_params=("counterId",),
)

# Query-параметры (openapi offline_conversions/upload_1, r21770580):
#   comment — комментарий к загрузке, ≤255 символов, опциональный;
#   type — BASIC (default) | CALLS | CHATS.
# client_id_type из вендорного маппинга 2022 в текущем openapi ОТСУТСТВУЕТ —
# не передаётся. Формат CSV — гайд «Офлайн-конверсии»:
# https://yandex.ru/dev/metrika/ru/management/offline-conv.md
