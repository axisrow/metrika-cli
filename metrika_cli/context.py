"""Общий контекст для команд CLI: глобальные опции и фабрика ресурсов.

Хранит токен/base-url/output в ``ctx.obj`` (Typer/Click) и по требованию
создаёт :class:`Client`. Здесь же — единый декоратор обработки ошибок API,
чтобы команды оставались тонкими.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import Any, Callable, Optional

import typer

from .config import ConfigError, load_config
from .client import APIError, Client
from .output import print_error


@dataclass
class AppState:
    """Глобальные опции, заполняются в главном callback."""

    token: Optional[str] = None
    base_url: Optional[str] = None
    output: str = "json"  # json | table
    pretty: bool = False

    def client(self) -> Client:
        config = load_config(token=self.token, base_url=self.base_url)
        return Client(config)


def get_state(ctx: typer.Context) -> AppState:
    if ctx.obj is None:
        ctx.obj = AppState()
    return ctx.obj


def handle_errors(func: Callable) -> Callable:
    """Превратить ConfigError/APIError в аккуратный exit(1) вместо трейсбека."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (APIError, ConfigError) as exc:
            print_error(str(exc))
            raise typer.Exit(code=1)

    return wrapper
