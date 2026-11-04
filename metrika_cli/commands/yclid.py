"""Каркас группы ``yclid`` — команд в группе нет.

Ресурс ``/management/v1/counter/{counterId}/yclid_conversions/`` (upload,
uploadings, uploading/{id} — как в вендорном маппинге 2022) удалён из API
Яндекс Метрики: по официальному changelog от 17.06.2020 заменён на
``/management/v1/counter/{counterId}/offline_conversions/uploadings``.
Живой OpenAPI эндпоинтов yclid_conversions не содержит (индекс llms.txt —
ни одного yclid-эндпоинта; страницы openapi/yclid-conversion/* отвечают 404).
YCLID-конверсии передаются как офлайн-конверсии с ``client_id_type=YCLID``
(POST multipart ``…/offline_conversions/upload``) — это группа ``conversions``
(issue #8). Registry/api для несуществующих путей не заводятся.
"""

from __future__ import annotations

import typer

app = typer.Typer(
    help=(
        "Пустая группа: API yclid_conversions удалён Яндексом (17.06.2020); "
        "YCLID-конверсии передаются через `metrika conversions` "
        "(client_id_type=YCLID)."
    ),
    no_args_is_help=True,
)
