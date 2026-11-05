"""Восстановление удалённого счётчика

POST /management/v1/counter/{counterId}/undelete

Подтверждено официальным openapi
(management/openapi/counter/undeleteCounter.md, ревизия r21770580).
"""

from .._core import Endpoint, GROUP_COUNTERS

ENDPOINT = Endpoint(
    GROUP_COUNTERS,
    "undelete",
    "POST",
    "management/v1/counter/{counterId}/undelete",
    "Восстановить удалённый счётчик",
    path_params=("counterId",),
)
