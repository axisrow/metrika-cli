"""Создание списка товаров (CDP/CRM)

POST /cdp/api/v1/counter/{counterId}/schema/products

Подтверждено официальным openapi
(management/openapi/schema/createProducts.md, ревизия r21770580).
Тело {"attributes": [...], "items": [...]}.
"""

from .._core import Endpoint, GROUP_CDP

ENDPOINT = Endpoint(
    GROUP_CDP,
    "create_products",
    "POST",
    "cdp/api/v1/counter/{counterId}/schema/products",
    "Создать список товаров",
    path_params=("counterId",),
)
