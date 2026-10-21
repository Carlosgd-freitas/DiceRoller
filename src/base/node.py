"""Node module."""

from __future__ import annotations

from abc import abstractmethod
from enum import Enum
from typing import Any, List


class NodeType(Enum):
    """Type of Node."""

    BATTLE = "BATTLE"
    BOSS_BATTLE = "BOSS_BATTLE"


class Node:
    """
    Node class.

    :var label: Node label.
    :vartype label: str

    :var type: Node type.
    :vartype type: NodeType

    :var path_level: At which Graph level (depth) the Node is found, starting from 1.
    :vartype path_level: int

    :var previous_nodes: Previous nodes in an Area path.
    :vartype previous_nodes: List[Node]

    :var next_nodes: Next nodes in an Area path.
    :vartype next_nodes: List[Node]
    """

    def __init__(
        self,
        label: str,
        type: NodeType,
        path_level: int,
        previous_nodes: List[Node] = None,
        next_nodes: List[Node] = None,
        **kwargs,
    ):
        self.label = label
        self.type = type
        self.path_level = path_level
        self.previous_nodes = [] if previous_nodes is None else previous_nodes
        self.next_nodes = [] if next_nodes is None else next_nodes

    def __str__(self) -> str:
        """String representation of Node."""
        _str = f"{self.label} ({self.type.value})"
        _str += f" | Path Level: {self.path_level}"

        if isinstance(self.previous_nodes, list) and len(self.previous_nodes) > 0:
            previous_nodes = ", ".join(
                [str(node.label) for node in self.previous_nodes]
            )
        else:
            previous_nodes = str(self.previous_nodes)
        _str += f" | Prev: {previous_nodes}"

        if isinstance(self.next_nodes, list) and len(self.next_nodes) > 0:
            next_nodes = ", ".join([str(node.label) for node in self.next_nodes])
        else:
            next_nodes = str(self.next_nodes)
        _str += f" | Next: {next_nodes}"

        return _str

    @abstractmethod
    def enter(self, **kwargs) -> Any:
        """
        Game behavior when a player enters the Node.
        """
        raise NotImplementedError
