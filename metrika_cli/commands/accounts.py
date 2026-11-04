"""Каркас группы ``accounts``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Аккаунты пользователя (Management API).", no_args_is_help=True)
