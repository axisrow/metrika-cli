"""Каркас группы ``grants``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Доступы к счётчику (Management API).", no_args_is_help=True)
