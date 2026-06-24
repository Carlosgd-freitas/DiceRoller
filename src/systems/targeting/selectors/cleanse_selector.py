"""Cleanse Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.systems.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class CleanseSelector(Selector):
    """
    Selects monster targets for the cleanse effect.
    """

    def get_targets_easy(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on EASY difficulty criteria for
        the cleanse effect:
        * 100% -> k monsters between self and alive allies that have the least debuffs

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)

        return self._get_targets_least_effects(
            monsters,
            k=k,
            effect_type=EffectType.DEBUFF,
            check_taunt=False,
        )

    def get_targets_normal(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on NORMAL difficulty criteria for
        the cleanse effect:
        * 30% -> k random monsters between self and alive allies
        * 70% -> k monsters between self and alive allies that have the most debuffs

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)

        if random() < 0.3:
            targets = self._get_targets_random(
                monsters,
                k=k,
                check_taunt=False,
            )

        else:
            targets = self._get_targets_most_effects(
                monsters,
                k=k,
                effect_type=EffectType.DEBUFF,
                check_taunt=False,
            )

        return targets

    def get_targets_hard(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on HARD difficulty criteria for
        the cleanse effect:
        * 100% -> k monsters between self and alive allies that have the most debuffs

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)

        return self._get_targets_most_effects(
            monsters,
            k=k,
            effect_type=EffectType.DEBUFF,
            check_taunt=False,
        )
