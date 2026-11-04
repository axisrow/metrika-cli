"""Каркас группы ``calls``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Офлайн-звонки (Data Import).", no_args_is_help=True)
