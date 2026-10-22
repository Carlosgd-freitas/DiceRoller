"""Node factory module."""

from typing import TYPE_CHECKING

from src.factories.factory import Factory
from src.registries.node import NodeRegistry

if TYPE_CHECKING:
    pass


class NodeFactory(Factory["Node"]):
    """Factory for creating nodes."""

    registries = NodeRegistry.load()
