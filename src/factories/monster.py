"""Monster factory module."""

from typing import TYPE_CHECKING

from src.factories.factory import Factory
from src.registries.monster import MonsterRegistry

if TYPE_CHECKING:
    pass


class MonsterFactory(Factory["Monster"]):
    """Factory for creating monsters."""

    registries = MonsterRegistry.load()
