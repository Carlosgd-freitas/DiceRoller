"""Selector Manager module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.difficulties import Difficulty
from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.targeting.selectors.buff_selector import BuffSelector
from src.targeting.selectors.debuff_selector import DebuffSelector
from src.targeting.selectors.defensive_selector import DefensiveSelector
from src.targeting.selectors.offensive_selector import OffensiveSelector
from src.targeting.selectors.random_selector import RandomSelector
from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.base.side import Side


class SelectorManager:
    def get_targets(
        self,
        side: Side,
        source: Monster,
        allies: List[Monster] = None,
        enemies: List[Monster] = None,
        k: int = 1,
        difficulty: Difficulty = Difficulty.NORMAL,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on Side's effects.

        :param side: A Side.
        :type side: Side

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param difficulty: What kind of strategy will be used to determine the targets.
        Harder difficulties means more smart strategies. Default value is Difficulty.NORMAL.
        :type difficulty: Difficulty

        :return: A list of target monsters.
        :rtype: List[Monster]
        """

        selector: Selector = None

        # Determining the main properties
        main_keyword = None
        main_effect_type = None
        main_count = 0

        for effect_type, keywords in side.get_effects_summary().items():
            if len(keywords) > main_count:
                main_keyword = keywords[0]
                main_effect_type = effect_type
                main_count = len(keywords)

        # Confuse check
        confused = source.get_effect(Keyword.CONFUSE)
        if confused and random() < confused.value:
            selector = RandomSelector()

        # Curse Effect
        for effect in side.effects:
            if effect.keyword == Keyword.CURSE:
                selector = DefensiveSelector()
                break

        if not selector:

            # Determining Selector
            if main_effect_type in [
                EffectType.DETERIORATION.value,
                EffectType.OFFENSIVE.value,
            ]:
                selector = OffensiveSelector()

            elif main_effect_type in [
                EffectType.DEFENSIVE.value,
                EffectType.RESTORATION.value,
            ]:
                selector = DefensiveSelector()

            elif main_effect_type == EffectType.BUFF.value:
                selector = BuffSelector()

            elif main_effect_type == EffectType.DEBUFF.value:
                selector = DebuffSelector()

            else:
                selector = RandomSelector()

        # Using get targets strategy
        if difficulty == Difficulty.EASY:
            targets = selector.get_targets_easy(
                source=source,
                allies=allies,
                enemies=enemies,
                k=k,
                main_keyword=main_keyword,
            )

        elif difficulty == Difficulty.NORMAL:
            targets = selector.get_targets_normal(
                source=source,
                allies=allies,
                enemies=enemies,
                k=k,
                main_keyword=main_keyword,
            )

        else:
            targets = selector.get_targets_hard(
                source=source,
                allies=allies,
                enemies=enemies,
                k=k,
                main_keyword=main_keyword,
            )

        return targets
