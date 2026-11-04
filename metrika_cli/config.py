"""Конфигурация клиента: токен, базовый URL, пространство имён API.

Источники токена (по приоритету):
1. явно переданный аргумент ``token``;
2. переменная окружения ``METRIKA_TOKEN``;
3. файл ``~/.config/metrika-cli/token`` (одна строка).

У Метрики несколько API с разными префиксами путей на одном хосте
(см. registry/_core.py): management/v1, api/v2/data, api/v2 — базовый
URL поэтому хостовый, а префикс живёт в пути каждого эндпоинта.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

#: Хост API (все API Метрики живут на одном хосте).
DEFAULT_BASE_URL = "https://api-metrika.yandex.net"

ENV_TOKEN = "METRIKA_TOKEN"
ENV_BASE_URL = "METRIKA_BASE_URL"

#: Путь к файлу с токеном по умолчанию.
TOKEN_FILE = Path.home() / ".config" / "metrika-cli" / "token"


class ConfigError(RuntimeError):
    """Ошибка конфигурации (например, отсутствует токен)."""


def _read_token_file() -> Optional[str]:
    try:
        text = TOKEN_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return text or None


@dataclass(frozen=True)
class Config:
    """Неизменяемая конфигурация клиента."""

    token: str
    base_url: str = DEFAULT_BASE_URL


def resolve_token(token: Optional[str] = None) -> str:
    """Найти OAuth-токен по приоритету источников или поднять ConfigError."""
    candidate = token or os.environ.get(ENV_TOKEN) or _read_token_file()
    if not candidate:
        raise ConfigError(
            "OAuth-токен не найден. Передайте --token, задайте переменную "
            f"{ENV_TOKEN} или запишите токен в {TOKEN_FILE}."
        )
    return candidate.strip()


def load_config(token: Optional[str] = None, base_url: Optional[str] = None) -> Config:
    """Собрать :class:`Config` из аргументов и окружения."""
    return Config(
        token=resolve_token(token),
        base_url=base_url or os.environ.get(ENV_BASE_URL) or DEFAULT_BASE_URL,
    )
