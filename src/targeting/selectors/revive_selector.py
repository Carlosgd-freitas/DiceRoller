"""Revive Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.keywords import Keyword
    from src.base.monster import Monster


class ReviveSelector(Selector):
    """
    Selects monster targets for the revive effect.
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
        the revive effect:
        * 100% -> k dead allies with least max hp

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
        targets: List[Monster] = []

        targets = self._get_targets_lowest_max_hp(
            allies,
            k=k,
            life_state="DEAD",
            check_taunt=False,
        )

        return targets

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
        the revive effect:
        * 100% -> k random, dead allies

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
        targets: List[Monster] = []

        targets = self._get_targets_random(
            allies,
            k=k,
            life_state="DEAD",
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
        the revive effect:
        * 10% -> k random, dead allies
        * 90% -> k dead allies with most max hp

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
        targets: List[Monster] = []

        if random() < 0.1:
            targets = self._get_targets_random(
                allies,
                k=k,
                life_state="DEAD",
                check_taunt=False,
            )

        else:
            targets = self._get_targets_highest_max_hp(
                allies,
                k=k,
                life_state="DEAD",
                check_taunt=False,
            )

        return targets
