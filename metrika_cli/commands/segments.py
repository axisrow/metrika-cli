"""Каркас группы ``segments``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Сегменты счётчика (Management API).", no_args_is_help=True)
