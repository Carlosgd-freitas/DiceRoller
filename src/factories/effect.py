"""Effect factory module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.keywords import Keyword
from src.factories.factory import Factory
from src.registries.effect import EffectRegistry

if TYPE_CHECKING:
    from src.base.effect import Effect

REGISTRIES = EffectRegistry.load()


class EffectFactory(Factory):
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

    @staticmethod
    def get_all_objects() -> List[Effect]:
        """
        Gets all Effects instantiable by the factory.

        :return: A list of all effects.
        :rtype: List[Effect]
        """
        objs = []

        for key in REGISTRIES.keys():
            obj = EffectFactory.create(key)
            objs.append(obj)

        return objs
