"""metrika — CLI для API Яндекс Метрики.

Точка входа и сборка корневого Typer-приложения. Зеркалит структуру
API Метрики «1 в 1»: три группы команд = три API:
- stat     → Reports API (/stat/v1): table, bytime, comparison, drilldown, pivot;
- counters → Management API (/management/v1): CRUD счётчиков;
- logs     → Logs API (/management/v1/counter/{id}/logrequest…): выгрузка сырых данных.

Единый источник правды по эндпоинтам — registry/.

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
from .commands import logs as logs_cli
from .commands import stat as stat_cli

app = typer.Typer(
    name="metrika",
    help=(
        "CLI для API Яндекс Метрики — stat (отчёты), counters (Management), "
        f"logs (сырые данные). {len(registry.ENDPOINTS)} эндпоинтов."
    ),
    no_args_is_help=True,
    add_completion=True,
)

# Под-приложения = API Метрики.
app.add_typer(counters_cli.app, name="counters")
app.add_typer(logs_cli.app, name="logs")
app.add_typer(stat_cli.app, name="stat")


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
        None, "--base-url", envvar=ENV_BASE_URL, help="Базовый URL API (для тестов/прокси)."
    ),
    output: str = typer.Option(
        "json", "--output", "-o", help="Формат вывода: json | table."
    ),
    pretty: bool = typer.Option(
        False, "--pretty", help="Запрашивать pretty-ответ у API."
    ),
    _version: bool = typer.Option(
        False, "--version", callback=_version_callback, is_eager=True, help="Версия CLI."
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
