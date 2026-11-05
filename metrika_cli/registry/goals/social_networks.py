"""Список социальных сетей (справочник для целей-соцсетей)

GET /management/v1/social_networks

Подтверждено официальным openapi
(management/openapi/goal/getSocialNetworks.md, ревизия r21770580).
Параметров нет; ответ {"social_networks": [...]}.
"""

from .._core import Endpoint, GROUP_GOALS

ENDPOINT = Endpoint(
    GROUP_GOALS,
    "social_networks",
    "GET",
    "management/v1/social_networks",
    "Справочник социальных сетей",
)
