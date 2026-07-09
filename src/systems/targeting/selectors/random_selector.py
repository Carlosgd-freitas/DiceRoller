"""Random Selector module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.systems.targeting.filters import preprocess_enemies
from src.systems.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.keywords import Keyword
    from src.base.monster import Monster


class RandomSelector(Selector):
    """
    Selects monster targets randomly.
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
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            enemies = preprocess_enemies(enemies)
            monsters.extend(enemies)

        return self._get_targets_random(
            monsters=monsters,
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
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            enemies = preprocess_enemies(enemies)
            monsters.extend(enemies)

        return self._get_targets_random(
            monsters=monsters,
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
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            enemies = preprocess_enemies(enemies)
            monsters.extend(enemies)

        return self._get_targets_random(
            monsters=monsters,
            k=k,
        )
