"""Buff Selector module."""

from __future__ import annotations

from random import random
from typing import TYPE_CHECKING, List

from src.base.keywords import Keyword
from src.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class BuffSelector(Selector):
    """
    Selects monster targets for buff type effects.
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
        buff type effects:
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
        targets: List[Monster] = []

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    allies,
                    k=k - len(targets),
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
        buff type effects:
        * 50% -> self + (k-1) alive allies without the buff
        * 50% -> self + (k-1) alive allies with the buff

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

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            if random() < 0.5:
                targets.extend(
                    self._get_targets_without_effects(
                        allies,
                        k=k - len(targets),
                        effects=[main_keyword],
                    )
                )

            else:
                targets.extend(
                    self._get_targets_with_effects(
                        allies,
                        k=k - len(targets),
                        effects=[main_keyword],
                    )
                )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    allies,
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
        buff type effects:
        * 50% -> self + (k-1) alive allies without the buff
        * 50% -> self + (k-1) alive allies with the buff

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

        if len(targets) < k:
            targets.append(source)

        if len(targets) < k:
            if random() < 0.5:
                targets.extend(
                    self._get_targets_without_effects(
                        allies,
                        k=k - len(targets),
                        effects=[main_keyword],
                    )
                )

            else:
                targets.extend(
                    self._get_targets_with_effects(
                        allies,
                        k=k - len(targets),
                        effects=[main_keyword],
                    )
                )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    allies,
                    k=k - len(targets),
                    exclude=[target.local_id for target in targets],
                )
            )

        return targets
