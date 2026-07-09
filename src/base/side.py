"""Side module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect


class Side:
    """
    Side class.

    :var effects: Side's effects, which will be executed in order.
    :vartype effects: List[Effect]

    :var weight: Side's weight when rolling a dice. Default value is 1.
    :vartype weight: float
    """

    def __init__(self, effects: List[Effect], weight: float = 1):
        self.effects = effects
        self.weight = weight

    def __str__(self) -> str:
        """String representation of Side."""
        _str = f"Effects ({len(self.effects)}):"

        for effect in self.effects:
            _str += f"\n* {effect}"

        _str += f"\n* Weight: {self.weight}"

        return _str

    def has_effect(self, keyword: Keyword) -> bool:
        """
        Returns if the entity is currently under the effect.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: If the entity has the effect.
        :rtype: bool
        """
        for effect in self.effects:
            if effect.keyword == keyword:
                return True
        return False

    def get_effect(self, keyword: Keyword) -> Effect | None:
        """
        Returns an effect from the entity.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: An effect.
        :rtype: Effect
        """
        for effect in self.effects:
            if effect.keyword == keyword:
                return effect
        return None

    def get_effect_summary(self) -> Dict:
        """
        Gets a summary of the Side's effects based on their types.

        :return: A dictionary where the keys are effect types and the values are lists
        containing the keywords of the effects.
        :rtype: Dict
        """
        types = {}

        for effect in self.effects:
            if effect.type.value not in types:
                types[effect.type.value] = [effect.keyword]
            else:
                types[effect.type.value].append(effect.keyword)

        return types
