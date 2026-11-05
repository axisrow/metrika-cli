"""Реестр эндпоинтов: единый источник правды по путям API Метрики.

Эндпоинты объявляются по файлу на каждый: ``registry/<group>/<op>.py`` с
переменной ``ENDPOINT``. Здесь дерево автозагружается в плоский список
``ENDPOINTS`` и строится индекс ``GROUPED``.
"""

from __future__ import annotations

from typing import Dict, List

from ._core import (
    Endpoint,
    GROUPS,
    GROUP_COUNTERS,
    GROUP_GOALS,
    GROUP_GRANTS,
    GROUP_FILTERS,
    GROUP_OPERATIONS,
    GROUP_DELEGATES,
    GROUP_ACCOUNTS,
    GROUP_STAT,
    GROUP_LOGS,
    GROUP_CONVERSIONS,
    GROUP_CALLS,
    GROUP_EXPENSES,
    GROUP_USER_PARAMS,
    GROUP_SEGMENTS,
    GROUP_LABELS,
    GROUP_ANNOTATIONS,
    GROUP_ACCESS_FILTERS,
    GROUP_CLIENTS,
    GROUP_MEASUREMENT,
    GROUP_YCLID,
    by_group,
    get,
    render_path,
    _load,
)
from . import _core

#: Все эндпоинты (собирается автозагрузкой дерева registry/<group>/<op>.py).
ENDPOINTS: List[Endpoint] = _load(f"{__name__}")

#: Эндпоинты по группам (для --help, документации и тестов-стражей).
GROUPED: Dict[str, List[Endpoint]] = by_group(ENDPOINTS, GROUPS)


def get_endpoint(group: str, op: str) -> Endpoint:
    return get(ENDPOINTS, group, op)


__all__ = [
    "Endpoint",
    "ENDPOINTS",
    "GROUPED",
    "GROUPS",
    "GROUP_COUNTERS",
    "GROUP_GOALS",
    "GROUP_GRANTS",
    "GROUP_FILTERS",
    "GROUP_OPERATIONS",
    "GROUP_DELEGATES",
    "GROUP_ACCOUNTS",
    "GROUP_STAT",
    "GROUP_LOGS",
    "GROUP_CONVERSIONS",
    "GROUP_CALLS",
    "GROUP_EXPENSES",
    "GROUP_USER_PARAMS",
    "GROUP_SEGMENTS",
    "GROUP_LABELS",
    "GROUP_ANNOTATIONS",
    "GROUP_ACCESS_FILTERS",
    "GROUP_CLIENTS",
    "GROUP_MEASUREMENT",
    "GROUP_YCLID",
    "get_endpoint",
    "get",
    "render_path",
    "by_group",
    "_core",
]
