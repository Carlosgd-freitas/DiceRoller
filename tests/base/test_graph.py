"""Tests for Graph and GraphConfig classes."""

from src.base.graph import Graph, GraphConfig
from src.nodes.battle_node import BattleNode
from tests.utils import assert_conditions


def test_graph_config_get_n_nodes():
    config = GraphConfig()

    conditions = [
        config.get_n_nodes(config.end_nodes) == 1,
        config.get_n_nodes(config.start_nodes) >= 1,
        config.get_n_nodes(config.start_nodes) <= 3,
    ]

    assert_conditions(conditions)


def test_graph_get_nodes():
    nodes = {
        "A": BattleNode(label="A", path_level=1),
        "B": BattleNode(label="B", path_level=2),
    }

    graph = Graph(nodes=nodes)

    nodes = graph.get_nodes()

    conditions = [
        len(nodes) == 2,
    ]

    nodes = graph.get_nodes(path_level=2)

    conditions.extend(
        [
            len(nodes) == 1,
            nodes[0].label == "B",
        ]
    )

    assert_conditions(conditions)


def test_graph_add_path_simple():
    node_a = BattleNode(label="A", path_level=1)
    node_b = BattleNode(label="B", path_level=2)

    nodes = {
        "A": node_a,
        "B": node_b,
    }

    config = GraphConfig()
    graph = Graph(nodes=nodes)

    graph.add_path(config, start_node=node_a, end_node=node_b, label="C")

    nodes = graph.get_nodes()

    conditions = [
        len(nodes) == 2,
        node_a.next_nodes == [node_b],
        node_b.next_nodes == [],
        node_a.previous_nodes == [],
        node_b.previous_nodes == [node_a],
    ]

    assert_conditions(conditions)


def test_graph_add_path_sequential():
    node_a = BattleNode(label="A", path_level=1)
    node_b = BattleNode(label="B", path_level=3)

    nodes = {
        "A": node_a,
        "B": node_b,
    }

    config = GraphConfig()
    graph = Graph(nodes=nodes)

    graph.add_path(config, start_node=node_a, end_node=node_b, label="C")

    nodes = graph.get_nodes()
    node_c = graph.get_nodes(path_level=2)[0]

    conditions = [
        len(nodes) == 3,
        node_a.next_nodes == [node_c],
        node_c.next_nodes == [node_b],
        node_b.next_nodes == [],
        node_b.previous_nodes == [node_c],
        node_c.previous_nodes == [node_a],
        node_a.previous_nodes == [],
    ]

    assert_conditions(conditions)


def test_graph_add_path_branch():
    node_a = BattleNode(label="A", path_level=1)
    node_b = BattleNode(label="B", path_level=1)
    node_c = BattleNode(label="C", path_level=3)

    nodes = {
        "A": node_a,
        "B": node_b,
        "C": node_c,
    }

    config = GraphConfig()
    config.chance_existing_node = 0
    graph = Graph(nodes=nodes)

    graph.add_path(config, start_node=node_a, end_node=node_c, label="D")
    graph.add_path(config, start_node=node_b, end_node=node_c, label="E")

    nodes = graph.get_nodes()
    node_d = graph.get_nodes(path_level=2)[0]
    node_e = graph.get_nodes(path_level=2)[1]

    conditions = [
        len(nodes) == 5,
        node_a.next_nodes == [node_d],
        node_d.next_nodes == [node_c],
        node_b.next_nodes == [node_e],
        node_e.next_nodes == [node_c],
        node_c.next_nodes == [],
        node_c.previous_nodes == [node_d, node_e],
        node_d.previous_nodes == [node_a],
        node_e.previous_nodes == [node_b],
        node_a.previous_nodes == [],
        node_b.previous_nodes == [],
    ]

    assert_conditions(conditions)


def test_graph_generate():
    config = GraphConfig()
    config.start_nodes = (1, 1)

    graph = Graph()

    graph.generate(config)

    conditions = [
        len(graph.get_nodes()) == 5,
        len(graph.get_nodes(path_level=1)) == 1,
        len(graph.get_nodes(path_level=2)) == 1,
        len(graph.get_nodes(path_level=3)) == 1,
        len(graph.get_nodes(path_level=4)) == 1,
        len(graph.get_nodes(path_level=5)) == 1,
    ]

    assert_conditions(conditions)
