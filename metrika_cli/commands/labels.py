"""Каркас группы ``labels``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(
    help="Метки и привязка к счётчикам (Management API).", no_args_is_help=True
)
