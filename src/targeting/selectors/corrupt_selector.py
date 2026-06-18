"""Corrupt Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class CorruptSelector(Selector):
    """
    Selects monster targets for the corrupt effect.
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
        the corrupt effect:
        * 100% -> k alive enemies that have the least buffs

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
        enemies = self._preprocess_enemies(enemies)

        return self._get_targets_least_effects(
            enemies,
            k=k,
            effect_type=EffectType.BUFF,
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
        the corrupt effect:
        * 30% -> k random alive enemies
        * 70% -> k alive enemies that have the most buffs

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
        enemies = self._preprocess_enemies(enemies)

        if random() < 0.3:
            targets = self._get_targets_random(
                enemies,
                k=k,
            )

        else:
            targets = self._get_targets_most_effects(
                enemies,
                k=k,
                effect_type=EffectType.BUFF,
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
        the corrupt effect:
        * 100% -> k alive enemies that have the most buffs

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
        enemies = self._preprocess_enemies(enemies)

        return self._get_targets_most_effects(
            enemies,
            k=k,
            effect_type=EffectType.BUFF,
        )
