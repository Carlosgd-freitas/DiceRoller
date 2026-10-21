"""Graph module."""

from dataclasses import dataclass, field
from random import choice, random
from typing import Dict, List, Tuple

from src.base.node import Node, NodeType
from src.combat.suffixes import SuffixManager
from src.nodes.battle_node import BattleNode
from src.nodes.boss_battle_node import BossBattleNode


@dataclass
class GraphConfig:
    """
    GraphConfig dataclass.

    :param start_nodes: Generated Graph will have a number of starting nodes in this
    closed interval. Default value is [1, 3].
    :type start_nodes: Tuple[int, int]

    :param end_nodes: Generated Graph will have a number of ending nodes in this
    closed interval. Default value is [1, 1].
    :type end_nodes: Tuple[int, int]

    :param node_types: Possible node types. By default, battles are boss batles are
    considered.
    :type node_types: List[NodeType]

    :param max_length: Maximum path length that can be transversed by the player.
    Default value is 5.
    :type max_length: int

    :param chance_existing_node: Chance for choosing existing nodes when adding paths
    in Graph generation.
    :type chance_existing_node: float
    """

    start_nodes: Tuple[int, int] = (1, 3)
    end_nodes: Tuple[int, int] = (1, 1)
    node_types: List[NodeType] = field(
        default_factory=lambda: [
            NodeType.BATTLE,
            NodeType.BOSS_BATTLE,
        ]
    )
    max_length: int = 5
    chance_existing_node: float = 0.6

    def get_n_nodes(self, param: Tuple[int, int]) -> int:
        """
        Returns an appropriate number of nodes based on a configuration parameter.

        :var param: A GraphConfig parameter that can define a number of nodes
        (e.g. `start_nodes`).
        :vartype param: Tuple[int, int]

        :return: Number of nodes.
        :rtype: int
        """
        if param[0] > param[1]:
            raise ValueError("param min value is higher than max value.")

        n = choice(range(param[0], param[1] + 1))
        return n


class Graph:
    """
    Graph class.

    :var nodes: Dictionary containing the Graph Nodes, where each key is .
    :vartype nodes: Dict

    :var suffix_manager: Manager for Area Nodes labels.
    :vartype suffix_manager: SuffixManager
    """

    def __init__(
        self,
        nodes: Dict = None,
        suffix_manager: SuffixManager = None,
        **kwargs,
    ):
        self.nodes = {} if nodes is None else nodes
        self.suffix_manager = suffix_manager or SuffixManager()

    def create_node(self, node_type: NodeType, **kwargs) -> Node:
        """
        Instantiates a Node from a register by its type.

        :param node_type: Node type.
        :type node_type: NodeType

        :return: Instantiated Node.
        :rtype: Node
        """
        if node_type == NodeType.BATTLE:
            return BattleNode(**kwargs)
        elif node_type == NodeType.BOSS_BATTLE:
            return BossBattleNode(**kwargs)

    def get_nodes(self, path_level: int = None) -> List[Node]:
        """
        Returns Nodes from a Graph, with optional filter options.

        :param path_level: Only Nodes with the same path level will be returned.
        :type path_level: int

        :return: Graph Nodes which meet the criteria.
        :rtype: List[Node]
        """
        nodes: List[Node] = [node for _, node in self.nodes.items()]

        if path_level:
            nodes = [node for node in nodes if node.path_level == path_level]

        return nodes

    def add_path(
        self,
        config: GraphConfig,
        start_node: Node,
        end_node: Node,
        label: str,
    ) -> str:
        """
        Adds a path to the Graph from a Node to another.

        :param config: Graph configuration.
        :type config: GraphConfig

        :param start_node: Where the path will start.
        :type start_node: Node

        :param end_node: Where the path will end.
        :type end_node: Node

        :param label: Starting label for the Nodes that can be created for the path.
        :type label: Node

        :return: Ending label for the Nodes that can be created for future paths.
        :rtype: str
        """
        current_node: Node = start_node

        while current_node.path_level < end_node.path_level:
            next_level = current_node.path_level + 1

            # Next node is the end node
            if next_level == end_node.path_level:
                next_node = end_node

            # Next node is an intermediary node
            else:
                nodes = self.get_nodes(path_level=next_level)

                next_node: Node
                # Deciding the intermediary node
                if len(nodes) > 0 and random() <= config.chance_existing_node:
                    next_node = choice(nodes)

                else:
                    next_node = self.create_node(
                        NodeType.BATTLE,
                        label=label,
                        path_level=next_level,
                    )
                    self.nodes[label] = next_node
                    label = self.suffix_manager.increase_suffix(label)

            # Connecting current node to the next node
            if next_node not in current_node.next_nodes:
                current_node.next_nodes.append(next_node)
            if current_node not in next_node.previous_nodes:
                next_node.previous_nodes.append(current_node)

            current_node = next_node

        return label

    def generate(
        self,
        config: GraphConfig | None = None,
    ):
        """
        Clears the current Nodes and paths between them, if any, and create new ones.

        :param config: Graph Configuration.
        :type config: GraphConfig
        """
        self.nodes = {}

        config = config or GraphConfig()
        label = "A"
        non_end_node_types = list(set(config.node_types) - set([NodeType.BOSS_BATTLE]))

        # Start Nodes
        start_node_type = (
            NodeType.BATTLE
            if NodeType.BATTLE in non_end_node_types
            else choice(non_end_node_types)
        )
        n_start_nodes = config.get_n_nodes(config.start_nodes)
        start_nodes: List[Node] = []

        for _ in range(n_start_nodes):
            node = self.create_node(start_node_type, label=label, path_level=1)
            start_nodes.append(node)
            self.nodes[label] = node
            label = self.suffix_manager.increase_suffix(label)

        # End Nodes
        end_node_type = (
            NodeType.BOSS_BATTLE
            if NodeType.BOSS_BATTLE in config.node_types
            else choice(config.node_types)
        )
        n_end_nodes = config.get_n_nodes(config.end_nodes)
        end_nodes: List[Node] = []

        for _ in range(n_end_nodes):
            node = self.create_node(
                end_node_type, label=label, path_level=config.max_length
            )
            end_nodes.append(node)
            self.nodes[label] = node
            label = self.suffix_manager.increase_suffix(label)

        # Intermediary Nodes + Paths
        for start_node in start_nodes:
            for end_node in end_nodes:
                label = self.add_path(
                    config=config,
                    start_node=start_node,
                    end_node=end_node,
                    label=label,
                )

        return
