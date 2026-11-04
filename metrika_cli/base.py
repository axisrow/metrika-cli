"""Базовый класс ресурса.

Связывает группу ресурса с реестром эндпоинтов и предоставляет хелпер
:meth:`Resource._call`, который берёт описание эндпоинта из registry
(HTTP-метод и путь) — так слой ресурсов не дублирует строки путей.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional

from . import registry
from .client import Client


class Resource:
    """Базовый ресурс. Подклассы задают ``group``."""

    group: str = ""

    def __init__(self, client: Client) -> None:
        self._client = client

    def _call(
        self,
        op: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        files: Optional[Mapping[str, Any]] = None,
        pretty: bool = False,
        path_suffix: str = "",
        raw: bool = False,
        **path_params: object,
    ) -> Any:
        """Выполнить вызов эндпоинта ``self.group``/``op`` из реестра.

        ``path_suffix`` — расширение после пути (stat API выбирает формат
        ответа расширением: ``data.csv``); ``raw`` — вернуть текст ответа.
        """
        ep = registry.get_endpoint(self.group, op)
        path = registry.render_path(ep, **path_params) + path_suffix
        return self._client.request(
            ep.method,
            path,
            params=params,
            json=json,
            files=files,
            pretty=pretty,
            raw=raw,
        )

    def _upload(
        self,
        op: str,
        file_path: str,
        *,
        field: str = "file",
        params: Optional[Mapping[str, Any]] = None,
        pretty: bool = False,
        **path_params: Any,
    ) -> Any:
        """Multipart-загрузка файла (Data Import) через эндпоинт ``group/op``.

        Общий хелпер для всех upload-эндпоинтов Data Import (офлайн-конверсии,
        звонки, расходы, user params): файл уходит частью ``files={field: …}``
        с MIME ``text/csv``, остальное — как в :meth:`_call` (registry-путь,
        query-параметры, pretty).

        :param op: имя операции в registry (эндпоинт с ``multipart=True``).
        :param file_path: путь к CSV-файлу на диске.
        :param field: имя form-поля с файлом (в API Метрики обычно ``file``).
        """
        path = Path(file_path)
        with path.open("rb") as fh:
            files = {field: (path.name, fh, "text/csv")}
            return self._call(
                op, files=files, params=params, pretty=pretty, **path_params
            )
