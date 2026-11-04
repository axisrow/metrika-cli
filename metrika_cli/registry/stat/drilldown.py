"""Drill down (иерархия группировок)

GET /stat/v1/data/drilldown

Развернуть дерево группировок; фильтрация — по ID, не по именам.
"""

from .._core import Endpoint, GROUP_STAT

ENDPOINT = Endpoint(
    GROUP_STAT,
    "drilldown",
    "GET",
    "stat/v1/data/drilldown",
    "Иерархический отчёт (drill down по группировкам)",
)
