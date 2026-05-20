"""Defensive Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.targeting.filters import filter
from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.keywords import Keyword
    from src.base.monster import Monster


class DefensiveSelector(Selector):
    """
    Selects monster targets for defensive type effects.
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
        defensive type effects:
        * 100% -> self + (k-1) random, alive allies

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
        targets = []

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            targets.extend(
                filter(
                    allies,
                    k=k - len(targets),
                    method="RANDOM",
                    alive=True,
                )
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
        defensive type effects:
        * 20% -> self + (k-1) random, alive allies
        * 80% -> self + (k-1) alive allies with least hp

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
        targets = []

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            if random() < 0.2:
                targets.extend(
                    filter(
                        allies,
                        k=k - len(targets),
                        method="RANDOM",
                        alive=True,
                    )
                )

            else:
                targets.extend(
                    filter(
                        allies,
                        k=k - len(targets),
                        method="FIRST",
                        sort_function=(lambda x: x.hp),
                        alive=True,
                    )
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
        defensive type effects:
        * 100% -> self + (k-1) alive allies with least hp

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
        targets = []

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            targets.extend(
                filter(
                    allies,
                    k=k - len(targets),
                    method="FIRST",
                    sort_function=(lambda x: x.hp),
                    alive=True,
                )
            )

        return targets
