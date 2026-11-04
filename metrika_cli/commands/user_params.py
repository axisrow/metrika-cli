"""Каркас группы ``user_params``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Параметры посетителей (Data Import).", no_args_is_help=True)
