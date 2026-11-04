"""Удалить представителя

DELETE /management/v1/delegate?user_login=<login>

РАСХОЖДЕНИЕ с формулировкой issue #6: там
``DELETE management/v1/delegate/{userLogin}`` (плейсхолдер в пути).
По openapi delegates/deleteDelegate и вендорному маппингу 2022
(_resource_mapping.py, ресурс ``delegate``) путь — без плейсхолдера,
логин передаётся ОБЯЗАТЕЛЬНЫМ query-параметром ``user_login``.
Зафиксировано по openapi.
"""

from .._core import Endpoint, GROUP_DELEGATES

ENDPOINT = Endpoint(
    GROUP_DELEGATES,
    "delete",
    "DELETE",
    "management/v1/delegate",
    "Удалить представителя (query: user_login)",
)
