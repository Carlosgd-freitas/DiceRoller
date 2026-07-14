"""Side module."""

from __future__ import annotations

from collections import Counter
from typing import Dict, List

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword


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

    def get_main_effect_type(self) -> EffectType:
        """
        Gets the Side main effect type.

        :return: The main effect type of the Side.
        :rtype: EffectType
        """
        effect_types = [effect.type for effect in self.effects]
        counter = Counter(effect_types)

        most_frequent = counter.most_common(1)
        if most_frequent:
            return most_frequent[0][0]

    def get_main_keyword(self) -> Keyword:
        """
        Gets the Side main keyword.

        :return: The main keyword of the Side.
        :rtype: Keyword
        """
        keywords = [effect.keyword for effect in self.effects]
        counter = Counter(keywords)

        most_frequent = counter.most_common(1)
        if most_frequent:
            return most_frequent[0][0]

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

    def is_equivalent(self, side: Side) -> bool:
        """
        Compares two sides and returns if they are equivalent.

        :param side: Side for comparison.
        :type side: Side

        :return: If the sides are equivalent.
        :rtype: bool
        """
        return (
            isinstance(side, Side)
            and len(self.effects) == len(side.effects)
            and all(
                [
                    self_effect.is_equivalent(effect)
                    for self_effect, effect in zip(
                        self.effects, side.effects, strict=True
                    )
                ]
            )
            and self.weight == side.weight
        )
