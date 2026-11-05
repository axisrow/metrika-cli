"""Загрузка клиентов (CSV)

POST /cdp/api/v1/counter/{counterId}/data/contacts/csv

Подтверждено официальным openapi
(management/openapi/schema/uploadContacts.md, ревизия r21770580).
Multipart-файл (поле file) + query: columns_mapping (обязательный),
merge_mode (обязательный), delimiter_type. ВНИМАНИЕ: префикс /cdp/api/v1.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "upload_contacts",
    "POST",
    "cdp/api/v1/counter/{counterId}/data/contacts/csv",
    "Загрузка клиентов (CSV)",
    multipart=True,
    path_params=("counterId",),
)
