"""Загрузка клиентов (JSON)

POST /cdp/api/v1/counter/{counterId}/data/contacts/json

Подтверждено официальным openapi
(management/openapi/schema/uploadContactJson_1.md, ревизия r21770580).
Тело {"contacts": [...]}, merge_mode — обязательный query-параметр.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "upload_contacts_json",
    "POST",
    "cdp/api/v1/counter/{counterId}/data/contacts/json",
    "Загрузка клиентов (JSON)",
    path_params=("counterId",),
)
