"""Группа ``yclid``: API yclid_conversions удалён Яндексом (17.06.2020,
заменён на offline_conversions) — команд в группе нет. Проверяем честный
help и отсутствие эндпоинтов (сетевых вызовов нет, respx не нужен)."""

from typer.testing import CliRunner

from metrika_cli import registry
from metrika_cli.cli import app

runner = CliRunner()


def test_yclid_help_reports_removal() -> None:
    result = runner.invoke(app, ["yclid", "--help"])
    assert result.exit_code == 0
    assert "удалён" in result.output
    assert "client_id_type=YCLID" in result.output


def test_yclid_has_no_endpoints() -> None:
    """Страж: для удалённого ресурса не заводятся мёртвые эндпоинты."""
    assert [ep for ep in registry.ENDPOINTS if ep.group == "yclid"] == []
