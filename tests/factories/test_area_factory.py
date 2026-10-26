"""Tests for AreaFactory class."""

from __future__ import annotations

from src.areas.grasslands import Grasslands
from src.base.area import Area
from src.base.graph import Graph
from src.factories.area import AreaFactory
from src.nodes.battle_node import BattleNode
from tests.utils import assert_conditions


def test_area_factory_create_simple():
    area = AreaFactory.create("GRASSLANDS")

    conditions = [
        isinstance(area, Grasslands),
        area.id == "GRASSLANDS",
    ]

    assert_conditions(conditions)


def test_area_factory_create_args():
    graph = Graph(
        nodes={
            "A": BattleNode(label="A", path_level=1),
            "B": BattleNode(label="B", path_level=2),
        }
    )

    area = AreaFactory.create(
        "GRASSLANDS",
        graph=graph,
    )

    conditions = [
        isinstance(area, Area),
        area.id == "GRASSLANDS",
        area.graph == graph,
    ]

    assert_conditions(conditions)


def test_area_factory_get_all_objects():
    all_areas = AreaFactory.get_all_objects()

    conditions = [
        isinstance(all_areas, list),
        len(all_areas) > 0,
        all([isinstance(area, Area) for area in all_areas]),
    ]

    assert_conditions(conditions)
