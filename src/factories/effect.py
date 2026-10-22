"""Effect factory module."""

from typing import TYPE_CHECKING

from src.factories.factory import Factory
from src.registries.effect import EffectRegistry

if TYPE_CHECKING:
    pass


class EffectFactory(Factory["Effect"]):
    """Factory for creating effects."""

    registries = EffectRegistry.load()
