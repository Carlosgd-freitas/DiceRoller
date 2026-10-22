"""Character factory module."""

from typing import TYPE_CHECKING

from src.factories.factory import Factory
from src.registries.character import CharacterRegistry

if TYPE_CHECKING:
    pass


class CharacterFactory(Factory["Character"]):
    """Factory for creating characters."""

    registries = CharacterRegistry.load()
