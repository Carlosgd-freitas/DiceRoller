"""Delay Selector module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectType
from src.factories.effect import EffectFactory
from src.systems.targeting.selectors.selector import Selector

if TYPE_CHECKING:
    from src.base.monster import Monster


class DelaySelector(Selector):
    """
    Selects monster targets for the delay effect.
    """

    def get_targets_easy(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on EASY difficulty criteria for
        the delay effect:
        * 100% -> k random alive monsters, among source, allies and enemies

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_effect: The main effect.
        :type main_effect: Effect

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            monsters.extend(enemies)

        return self._get_targets_random(
            monsters,
            k=k,
            consider=[],
        )

    def get_targets_normal(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on NORMAL difficulty criteria for
        the delay effect:
        * 100% -> k monsters with effects that can have their duration extended
        by the delay effect

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_effect: The main effect.
        :type main_effect: Effect

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        monsters = []
        if source:
            monsters.append(source)
        if allies:
            monsters.extend(allies)
        if enemies:
            monsters.extend(enemies)

        targets = self._get_targets_highest_hp(
            monsters,
            k=k,
            keyword_whitelist=main_effect.target_keywords,
            consider=[],
        )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    monsters,
                    k=k,
                    consider=[],
                )
            )

        return targets

    def get_targets_hard(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on HARD difficulty criteria for
        the delay effect:
        * 100% -> k monsters with the effects that can have their duration extended
        by the delay effect, prioritizing self and allies if the the later are
        benefitial or enemies otherwise

        :param source: The source monster which is targeting others.
        :type source: Monster

        :param allies: The source monster's allies.
        :type allies: List[Monster]

        :param enemies: The source monster's enemies.
        :type enemies: List[Monster]

        :param k: The number of monsters which will be returned.
        :type k: int

        :param main_effect: The main effect.
        :type main_effect: Effect

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        target_effects = [
            EffectFactory.create_effect(keyword)
            for keyword in main_effect.target_keywords
        ]

        effect_type = self._get_most_frequent_effect_types(
            target_effects,
            k=k,
        )[0]

        monsters = []

        if effect_type in [
            EffectType.BUFF,
            EffectType.CURSE,
            EffectType.DEFENSIVE,
            EffectType.RESTORATION,
        ]:
            if source:
                monsters.append(source)
            if allies:
                monsters.extend(allies)

        elif effect_type in [
            EffectType.DEBUFF,
            EffectType.DETERIORATION,
            EffectType.OFFENSIVE,
        ]:
            if enemies:
                monsters.extend(enemies)

        else:
            if source:
                monsters.append(source)
            if allies:
                monsters.extend(allies)
            if enemies:
                monsters.extend(enemies)

        targets = self._get_targets_highest_hp(
            monsters,
            k=k,
            keyword_whitelist=main_effect.target_keywords,
            consider=[],
        )

        if len(targets) < k:
            targets.extend(
                self._get_targets_random(
                    monsters,
                    k=k,
                    consider=[],
                )
            )

        return targets
