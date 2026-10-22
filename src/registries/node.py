"""Node registry module."""

from typing import TYPE_CHECKING, ClassVar

from src.registries.registry import Registry

if TYPE_CHECKING:
    from src.base.node import Node


class NodeRegistry(Registry["Node"]):
    """Registry for Node classes."""

    id_name: str = "type"
    dir_name: str = "nodes"
    registries: ClassVar[dict[str, type[Node]]] = {}
