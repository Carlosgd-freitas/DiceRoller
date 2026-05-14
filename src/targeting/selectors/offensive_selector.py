"""Offensive Selector module."""

from __future__ import annotations

from random import random
from src.base.keywords import Keyword
from typing import List, TYPE_CHECKING
from src.targeting.filters import filter
from src.targeting.selectors.selector import Selector

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
    ):
        """
        Returns a list of target monsters based on EASY difficulty criteria for
        offensive type effects:
        * 20% -> random alive enemies
        * 80% -> alive enemies with most hp

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
        if random() < 0.2:
            return filter(
                enemies,
                k=k,
                method="RANDOM",
                alive=True,
            )

        else:
            return filter(
                enemies,
                k=k,
                method="LAST",
                sort_function=(lambda x: x.hp),
                alive=True,
            )

    def get_targets_normal(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ):
        """
        Returns a list of target monsters based on NORMAL difficulty criteria for
        offensive type effects:
        * 20% -> random alive enemies
        * 80% -> alive enemies with least hp

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
        if random() < 0.2:
            return filter(
                enemies,
                k=k,
                method="RANDOM",
                alive=True,
            )

        else:
            return filter(
                enemies,
                k=k,
                method="FIRST",
                sort_function=(lambda x: x.hp),
                alive=True,
            )

    def get_targets_hard(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ):
        """
        Returns a list of target monsters based on HARD difficulty criteria for
        offensive type effects:
        * 20% -> random alive enemies
        * 80% -> alive enemies with least hp, wihout Block or Absorb

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
        if random() < 0.2:
            return filter(
                enemies,
                k=k,
                method="RANDOM",
                alive=True,
            )

        else:
            targets = filter(
                enemies,
                k=k,
                method="FIRST",
                sort_function=(lambda x: x.hp),
                alive=True,
                keyword_blacklist=[Keyword.ABSORB, Keyword.BLOCK]
            )

            if len(targets) < k:
                targets.extend(
                    filter(
                        enemies,
                        k=k-len(targets),
                        method="FIRST",
                        sort_function=(lambda x: x.hp),
                        alive=True,
                        local_id_blacklist=[target.local_id for target in targets],
                    )
                )

            return targets
