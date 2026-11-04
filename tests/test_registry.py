"""Юнит-проверки реестра эндпоинтов."""

import pytest

from metrika_cli import registry

pytestmark = pytest.mark.unit


def test_endpoints_loaded() -> None:
    assert len(registry.ENDPOINTS) == 22
    groups = {ep.group for ep in registry.ENDPOINTS}
    assert {"counters", "stat", "logs", "annotations"} <= groups


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
