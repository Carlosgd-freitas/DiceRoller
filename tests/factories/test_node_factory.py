"""Tests for NodeFactory class."""

from __future__ import annotations

from src.base.node import Node, NodeType
from src.factories.node import NodeFactory
from src.nodes.battle_node import BattleNode
from tests.utils import assert_conditions


def test_node_factory_create_simple():
    node = NodeFactory.create(NodeType.BATTLE)

    conditions = [
        isinstance(node, BattleNode),
        node.type == NodeType.BATTLE,
    ]

    assert_conditions(conditions)


def test_node_factory_create_args():
    previous_node = BattleNode(label="A", path_level=1)

    node = NodeFactory.create(
        NodeType.BATTLE,
        label="B",
        path_level=2,
        previous_nodes=[previous_node],
    )

    conditions = [
        isinstance(node, BattleNode),
        node.type == NodeType.BATTLE,
        node.label == "B",
        node.path_level == 2,
        node.previous_nodes == [previous_node],
    ]

    assert_conditions(conditions)


def test_node_factory_get_all_objects():
    all_nodes = NodeFactory.get_all_objects()

    conditions = [
        isinstance(all_nodes, list),
        len(all_nodes) > 0,
        all([isinstance(node, Node) for node in all_nodes]),
    ]

    assert_conditions(conditions)
