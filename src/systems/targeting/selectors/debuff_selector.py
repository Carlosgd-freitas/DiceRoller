"""Debuff Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.keywords import Keyword
from src.systems.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class DebuffSelector(Selector):
    """
    Selects monster targets for debuff type effects.
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
        debuff type effects:
        * 100% -> random alive enemies

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

        return self._get_targets_random(
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
        debuff type effects:
        * 50% -> alive enemies without the debuff
        * 50% -> alive enemies with the debuff

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

        if random() < 0.5:
            targets = self._get_targets_without_effects(
                enemies,
                k=k,
                effects=[main_keyword],
            )

        else:
            targets = self._get_targets_with_effects(
                enemies,
                k=k,
                effects=[main_keyword],
            )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    enemies,
                    k=k - len(targets),
                    exclude=[target.local_id for target in targets],
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
        debuff type effects:
        * 50% -> alive enemies without the debuff
        * 50% -> alive enemies with the debuff

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

        if random() < 0.5:
            targets = self._get_targets_without_effects(
                enemies,
                k=k,
                effects=[main_keyword],
            )

        else:
            targets = self._get_targets_with_effects(
                enemies,
                k=k,
                effects=[main_keyword],
            )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    enemies,
                    k=k - len(targets),
                    exclude=[target.local_id for target in targets],
                )
            )

        return targets
