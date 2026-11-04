"""Каркас группы ``filters``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Фильтры счётчика (Management API).", no_args_is_help=True)
