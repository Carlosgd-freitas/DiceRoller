"""Random Selector module."""

from __future__ import annotations

from typing import List, TYPE_CHECKING
from src.targeting.filters import filter
from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.base.keywords import Keyword


class RandomSelector(Selector):
    """
    Selects monster targets randomly.
    """

    def _get_targets_default(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_keyword: Keyword,
    ):
        """Private, utility function for other functions of the class."""
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            monsters.extend(enemies)

        return filter(
            monsters,
            k=k,
            method="RANDOM",
            alive=True,
        )

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
        Offensive type effects:
        * 100% -> random alive monters, among source, allies and enemies

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
        return self._get_targets_default(
            source=source,
            allies=allies,
            enemies=enemies,
            k=k,
            main_keyword=main_keyword,
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
        Offensive type effects:
        * 100% -> random alive monters, among source, allies and enemies

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
        return self._get_targets_default(
            source=source,
            allies=allies,
            enemies=enemies,
            k=k,
            main_keyword=main_keyword,
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
        Offensive type effects:
        * 100% -> random alive monters, among source, allies and enemies

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
        return self._get_targets_default(
            source=source,
            allies=allies,
            enemies=enemies,
            k=k,
            main_keyword=main_keyword,
        )
