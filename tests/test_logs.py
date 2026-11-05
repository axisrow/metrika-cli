"""Проверки logs create: параметры уходят в query, тела у запроса нет (issue 43).

Контракт createLogRequest (openapi, проверен 2026-11-05): date1, date2,
fields, source — обязательные query-параметры, attribution — необязательный;
JSON-тела у POST /logrequests нет.
"""

import json

import pytest
import respx
from typer.testing import CliRunner

from metrika_cli.api.logs import Logs
from metrika_cli.client import Client
from metrika_cli.config import Config

pytestmark = pytest.mark.integration

runner = CliRunner()
BASE = "https://api-metrika.yandex.net"
URL = f"{BASE}/management/v1/counter/42/logrequests"

BODY = {
    "source": "visits",
    "date1": "2026-10-01",
    "date2": "2026-10-31",
    "fields": ["ym:pv:dateTime", "ym:pv:URL"],
}


def make_client() -> Client:
    return Client(Config(token="T"))


# -- api ------------------------------------------------------------------------


@respx.mock
def test_create_params_in_query_no_body() -> None:
    route = respx.post(URL).respond(json={"log_request": {"request_id": 1}})
    with make_client() as c:
        payload = Logs(c).create(42, dict(BODY))
    assert payload == {"log_request": {"request_id": 1}}
    assert route.called

    req = respx.calls[-1].request
    assert req.method == "POST"
    assert req.url.params["date1"] == "2026-10-01"
    assert req.url.params["date2"] == "2026-10-31"
    assert req.url.params["source"] == "visits"
    # список fields склеивается в comma-separated строку (формат query)
    assert req.url.params["fields"] == "ym:pv:dateTime,ym:pv:URL"
    assert "attribution" not in req.url.params
    assert req.read() == b""  # тела у запроса нет


@respx.mock
def test_create_string_fields_and_attribution() -> None:
    respx.post(URL).respond(json={"log_request": {}})
    with make_client() as c:
        Logs(c).create(
            42, {**BODY, "fields": "ym:pv:dateTime", "attribution": "first"}
        )
    req = respx.calls[-1].request
    assert req.url.params["fields"] == "ym:pv:dateTime"
    assert req.url.params["attribution"] == "first"


@respx.mock
def test_create_none_values_dropped() -> None:
    respx.post(URL).respond(json={"log_request": {}})
    with make_client() as c:
        Logs(c).create(42, {**BODY, "attribution": None})
    req = respx.calls[-1].request
    assert "attribution" not in req.url.params


# -- CLI (offline, CliRunner + respx) -------------------------------------------


@respx.mock
def test_cli_create_e2e_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    """CliRunner → команда → api → respx: query вместо JSON-тела, без сети."""
    from metrika_cli.cli import app as root_app

    monkeypatch.setenv("METRIKA_TOKEN", "T")
    route = respx.post(URL).respond(json={"log_request": {"request_id": 7}})
    result = runner.invoke(
        root_app, ["logs", "create", "42", "--data", json.dumps(BODY)]
    )
    assert result.exit_code == 0, result.output
    assert route.called

    req = respx.calls[-1].request
    assert req.url.params["date1"] == "2026-10-01"
    assert req.url.params["fields"] == "ym:pv:dateTime,ym:pv:URL"
    assert req.read() == b""
    assert "log_request" in result.output


@respx.mock
def test_cli_create_via_data_stdin_file(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    """--data @файл: тот же query-контракт."""
    from metrika_cli.cli import app as root_app

    data_file = tmp_path / "req.json"
    data_file.write_text(json.dumps(BODY), encoding="utf-8")
    monkeypatch.setenv("METRIKA_TOKEN", "T")
    respx.post(URL).respond(json={"log_request": {}})
    result = runner.invoke(
        root_app, ["logs", "create", "42", "--data", f"@{data_file}"]
    )
    assert result.exit_code == 0, result.output
    assert respx.calls[-1].request.url.params["source"] == "visits"


def test_cli_create_rejects_non_object() -> None:
    """JSON-массив/строка в --data — ошибка параметра, без HTTP-запроса."""
    from metrika_cli.cli import app as root_app

    result = runner.invoke(root_app, ["logs", "create", "42", "--data", "[1,2]"])
    assert result.exit_code == 2
    assert "JSON-объект" in result.output + result.stderr


def test_cli_create_requires_data() -> None:
    from metrika_cli.cli import app as root_app

    result = runner.invoke(root_app, ["logs", "create", "42"])
    assert result.exit_code == 2


def test_cli_create_help_mentions_query_keys() -> None:
    from metrika_cli.commands import logs as logs_cli

    result = runner.invoke(logs_cli.app, ["create", "--help"])
    assert result.exit_code == 0
    assert "attribution" in result.output
