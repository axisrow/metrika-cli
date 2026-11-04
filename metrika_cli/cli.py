"""metrika — CLI для API Яндекс Метрики.

Точка входа и сборка корневого Typer-приложения. Зеркалит структуру
API Метрики «1 в 1»: одна группа команд = одна ресурсная группа
(порядок — :data:`registry.GROUPS`):
- management-ресурсы: counters, goals, filters, operations, grants, delegates,
  accounts, segments, labels, annotations, access_filters;
- stat → Reports API (/stat/v1); logs → Logs API;
- data-import: conversions, calls, expenses, user_params, yclid.

Каркасные группы без команд показывают справку (``no_args_is_help``); их
команды приходят в фичевых PR (issues 2–19). Единый источник правды по
эндпоинтам — registry/.

Запуск: ``metrika ...`` (консольный скрипт) или ``python -m metrika_cli ...``.
"""

from __future__ import annotations

from typing import Optional

import typer

from . import __version__
from .config import ENV_BASE_URL, ENV_TOKEN
from .context import AppState, get_state
from . import registry

from .commands import counters as counters_cli
from .commands import goals as goals_cli
from .commands import filters as filters_cli
from .commands import operations as operations_cli
from .commands import grants as grants_cli
from .commands import delegates as delegates_cli
from .commands import accounts as accounts_cli
from .commands import segments as segments_cli
from .commands import labels as labels_cli
from .commands import annotations as annotations_cli
from .commands import access_filters as access_filters_cli
from .commands import stat as stat_cli
from .commands import logs as logs_cli
from .commands import conversions as conversions_cli
from .commands import calls as calls_cli
from .commands import expenses as expenses_cli
from .commands import user_params as user_params_cli
from .commands import yclid as yclid_cli

app = typer.Typer(
    name="metrika",
    help=(
        "CLI для API Яндекс Метрики: stat (отчёты), counters/logs и каркасы "
        f"остальных групп. {len(registry.ENDPOINTS)} эндпоинтов."
    ),
    no_args_is_help=True,
    add_completion=True,
)

# Под-приложения = группы ресурсов, в порядке registry.GROUPS.
app.add_typer(counters_cli.app, name="counters")
app.add_typer(goals_cli.app, name="goals")
app.add_typer(filters_cli.app, name="filters")
app.add_typer(operations_cli.app, name="operations")
app.add_typer(grants_cli.app, name="grants")
app.add_typer(delegates_cli.app, name="delegates")
app.add_typer(accounts_cli.app, name="accounts")
app.add_typer(segments_cli.app, name="segments")
app.add_typer(labels_cli.app, name="labels")
app.add_typer(annotations_cli.app, name="annotations")
app.add_typer(access_filters_cli.app, name="access_filters")
app.add_typer(stat_cli.app, name="stat")
app.add_typer(logs_cli.app, name="logs")
app.add_typer(conversions_cli.app, name="conversions")
app.add_typer(calls_cli.app, name="calls")
app.add_typer(expenses_cli.app, name="expenses")
app.add_typer(user_params_cli.app, name="user_params")
app.add_typer(yclid_cli.app, name="yclid")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"metrika-cli {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    token: Optional[str] = typer.Option(
        None, "--token", envvar=ENV_TOKEN, help="OAuth-токен Яндекса."
    ),
    base_url: Optional[str] = typer.Option(
        None,
        "--base-url",
        envvar=ENV_BASE_URL,
        help="Базовый URL API (для тестов/прокси).",
    ),
    output: str = typer.Option(
        "json", "--output", "-o", help="Формат вывода: json | table."
    ),
    pretty: bool = typer.Option(
        False, "--pretty", help="Запрашивать pretty-ответ у API."
    ),
    _version: bool = typer.Option(
        False,
        "--version",
        callback=_version_callback,
        is_eager=True,
        help="Версия CLI.",
    ),
) -> None:
    """Общие опции применяются ко всем командам."""
    state = get_state(ctx)
    state.token = token
    state.base_url = base_url
    state.output = output
    state.pretty = pretty


__all__ = ["app", "AppState", "__version__"]


if __name__ == "__main__":
    app()
