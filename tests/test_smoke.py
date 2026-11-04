"""Дымовой прогон CLI без сети: структура, справка, версия."""

import pytest
from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.cli import app

runner = CliRunner()

pytestmark = pytest.mark.smoke


def test_help_ok() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for group in ("counters", "logs", "stat"):
        assert group in result.output


def test_group_help_ok() -> None:
    for group in ("counters", "logs", "stat"):
        result = runner.invoke(app, [group, "--help"])
        assert result.exit_code == 0


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "metrika-cli 0.0.1" in result.output


def test_no_args_shows_help() -> None:
    # no_args_is_help печатает справку; click завершает её кодом 2
    result = runner.invoke(app, [])
    assert result.exit_code in (0, 2)
    assert "Usage" in result.output


def test_all_registry_groups_registered() -> None:
    """Страж: каждая группа из registry.GROUPS зарегистрирована в CLI,
    видна в ``--help`` и вызывается без падения (каркас без команд
    показывает справку)."""
    registered = {group.name for group in app.registered_groups}
    assert registered == set(registry.GROUPS)
    root = runner.invoke(app, ["--help"])
    assert root.exit_code == 0
    for group in registry.GROUPS:
        assert group in root.output
        group_help = runner.invoke(app, [group, "--help"])
        assert group_help.exit_code == 0
        bare = runner.invoke(app, [group])
        # no_args_is_help печатает справку; click завершает её кодом 2
        assert bare.exit_code in (0, 2)
        assert "Usage" in bare.output
