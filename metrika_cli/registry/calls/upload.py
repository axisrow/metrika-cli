"""Загрузить офлайн-звонки

POST /management/v1/counter/{counterId}/offline_conversions/upload_calls
"""

from .._core import Endpoint, GROUP_CALLS

ENDPOINT = Endpoint(
    GROUP_CALLS,
    "upload",
    "POST",
    "management/v1/counter/{counterId}/offline_conversions/upload_calls",
    "Загрузить CSV-файл со звонками",
    multipart=True,
    path_params=("counterId",),
)

# Query-параметры (вендорный маппинг tapi-yandex-metrika, uploadcalls-docpage):
#   client_id_type — USER_ID | CLIENT_ID | YCLID, обязательный; comment,
#   new_goal_name — опциональные. В новом openapi (openapi/call/uploadCalls)
#   client_id_type как query-параметр не указан — там тип ID определяется
#   колонкой CSV (UserId/ClientId/Yclid), поэтому передаём всегда: старый
#   API-контракт требует его явно.
