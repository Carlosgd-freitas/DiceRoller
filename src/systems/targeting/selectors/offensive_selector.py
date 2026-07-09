"""Offensive Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.keywords import Keyword
from src.systems.targeting.filters import preprocess_enemies
from src.systems.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class OffensiveSelector(Selector):
    """
    Selects monster targets for offensive type effects.
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
        offensive type effects:
        * 50% -> random alive enemies
        * 50% -> alive enemies with most hp

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
        enemies = preprocess_enemies(enemies)

        if random() < 0.5:
            return self._get_targets_random(
                enemies,
                k=k,
            )

        else:
            return self._get_targets_highest_hp(
                enemies,
                k=k,
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
        offensive type effects:
        * 30% -> random alive enemies
        * 70% -> alive enemies with least effective hp and hp

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
        enemies = preprocess_enemies(enemies)

        if random() < 0.3:
            return self._get_targets_random(
                enemies,
                k=k,
            )

        else:
            return self._get_targets_lowest_hp(
                enemies,
                k=k,
            )

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
        offensive type effects:
        * 10% -> random alive enemies
        * 90% -> alive enemies without Invisible or Sacred Block effects, and least
        effective hp and hp

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
        enemies = preprocess_enemies(enemies)
        targets: List[Monster] = []

        if random() < 0.1:
            targets = self._get_targets_random(
                enemies,
                k=k,
            )

        else:
            targets = self._get_targets_lowest_hp(
                enemies,
                k=k,
                keyword_blacklist=[Keyword.INVISIBLE, Keyword.SACRED_BLOCK],
            )

            if len(targets) < k:
                targets.extend(
                    self._get_targets_lowest_hp(
                        enemies,
                        k=k - len(targets),
                        blacklist=targets,
                    )
                )

        return targets
