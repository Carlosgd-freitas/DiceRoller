"""Effect factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.keywords import Keyword
from src.registries.effect import REGISTRIES, EffectRegistry

if TYPE_CHECKING:
    from src.base.effect import Effect

EffectRegistry.load()


class EffectFactory:
    """
    EffectFactory class.
    """

    @staticmethod
    def create(
        keyword: Keyword,
        **kwargs,
    ) -> Effect:
        """
        Instantiates an Effect from a register by its keyword.

        :param keyword: Effect keyword.
        :type keyword: Keyword

        :return: Instantiated Effect.
        :rtype: Effect
        """

        effect_class = REGISTRIES.get(keyword)

        if effect_class is None:
            raise ValueError(f"No effect registered for keyword: {keyword}")

        return effect_class(**kwargs)
