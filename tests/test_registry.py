"""Юнит-проверки реестра эндпоинтов."""

from pathlib import Path

import pytest

from metrika_cli import registry

pytestmark = pytest.mark.unit


def test_endpoints_loaded() -> None:
    # Страж без хардкода счётчика: множество (group, op) реестра обязано
    # совпадать с фактическим деревом registry/<group>/<op>.py, так что
    # добавление эндпоинта не требует правки теста. Рассинхрон — файл без
    # ENDPOINT, дубль (group, op) или каталог вне GROUPS — роняет тест
    # (или импорт реестра, что тоже красный прогон).
    tree = Path(registry.__file__).parent
    file_keys = {
        (group.name, f.stem)
        for group in tree.iterdir()
        if group.is_dir() and not group.name.startswith("_")
        for f in group.glob("*.py")
        if not f.name.startswith("_") and f.name != "__init__.py"
    }
    registry_keys = {(ep.group, ep.op) for ep in registry.ENDPOINTS}
    assert file_keys == registry_keys
    groups = {ep.group for ep in registry.ENDPOINTS}
    assert {
        "counters",
        "goals",
        "stat",
        "logs",
        "segments",
        "labels",
        "annotations",
        "operations",
        "access_filters",
        "delegates",
        "accounts",
        "conversions",
    } <= groups


def test_paths_from_host_root() -> None:
    for ep in registry.ENDPOINTS:
        assert not ep.path.startswith("/")


def test_get_endpoint_unknown_op() -> None:
    with pytest.raises(KeyError):
        registry.get_endpoint("stat", "nope")


def test_render_path() -> None:
    ep = registry.get_endpoint("logs", "info")
    path = registry.render_path(ep, counterId=42, requestId=7)
    assert path == "management/v1/counter/42/logrequest/7"


def test_render_path_missing_param() -> None:
    ep = registry.get_endpoint("logs", "info")
    with pytest.raises(KeyError):
        registry.render_path(ep, counterId=42)
