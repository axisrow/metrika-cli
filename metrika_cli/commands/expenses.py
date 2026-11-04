"""Каркас группы ``expenses``: команды приходят в фичевых PR."""

from __future__ import annotations

import typer

app = typer.Typer(help="Загрузка расходов (Data Import).", no_args_is_help=True)
