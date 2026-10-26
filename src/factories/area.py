"""Area factory module."""

from typing import TYPE_CHECKING

from src.factories.factory import Factory
from src.registries.area import AreaRegistry

if TYPE_CHECKING:
    pass


class AreaFactory(Factory["Area"]):
    """Factory for creating areas."""

    registries = AreaRegistry.load()
