"""Tests for NodeRegistry class."""

from __future__ import annotations

from src.base.node import NodeType
from src.registries.node import NodeRegistry
from tests.utils import assert_conditions


def test_node_registry_integrity():
    REGISTRIES = NodeRegistry.load()

    conditions = [
        len(REGISTRIES.keys()) > 0,
        REGISTRIES.get("0") is None,
        REGISTRIES.get(NodeType.BATTLE) is not None,
        REGISTRIES.get(NodeType.BOSS_BATTLE) is not None,
    ]

    assert_conditions(conditions)
