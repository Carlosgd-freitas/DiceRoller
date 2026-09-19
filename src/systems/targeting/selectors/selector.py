"""Selector module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.systems.targeting.filters import (
    filter_effect_types,
    filter_monsters,
)

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Monster


class Selector(ABC):
    """
    Abstract class for selecting monster targets.
    """

    @abstractmethod
    def get_targets_easy(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on EASY difficulty criteria.

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
        raise NotImplementedError

    @abstractmethod
    def get_targets_normal(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on NORMAL difficulty criteria.

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
        raise NotImplementedError

    @abstractmethod
    def get_targets_hard(
        self,
        source: Monster,
        allies: List[Monster],
        enemies: List[Monster],
        k: int,
        main_effect: Effect,
    ) -> List[Monster]:
        """
        Returns a list of target monsters based on HARD difficulty criteria.

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
        raise NotImplementedError

    def _get_most_frequent_effect_types(
        self,
        effects: List[Effect],
        k: int,
    ) -> List[EffectType]:
        """
        Returns k effect types that are most frequent.
        """
        return filter_effect_types(
            effect_types=[effect.type for effect in effects],
            k=k,
            frequency_order="MOST",
        )

    def _get_least_frequent_effect_types(
        self,
        effects: List[Effect],
        k: int,
    ) -> List[EffectType]:
        """
        Returns k effect types that are least frequent.
        """
        return filter_effect_types(
            effect_types=[effect.type for effect in effects],
            k=k,
            frequency_order="LEAST",
        )

    def _get_targets_random(
        self,
        monsters: List[Monster],
        k: int,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k random monsters.
        """
        return filter_monsters(
            monsters,
            k=k,
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="RANDOM",
        )

    def _get_targets_highest_hp(
        self,
        monsters: List[Monster],
        k: int,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with most effective hp and hp.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (lambda entity: -entity.get_effective_hp()),
                (lambda entity: -entity.hp),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )

    def _get_targets_lowest_hp(
        self,
        monsters: List[Monster],
        k: int,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with least effective hp and hp.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (lambda entity: entity.get_effective_hp()),
                (lambda entity: entity.hp),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )

    def _get_targets_highest_max_hp(
        self,
        monsters: List[Monster],
        k: int,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with most max hp.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (lambda entity: -entity.max_hp),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )

    def _get_targets_lowest_max_hp(
        self,
        monsters: List[Monster],
        k: int,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with least max hp.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (lambda entity: entity.max_hp),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )

    def _get_targets_most_effects(
        self,
        monsters: List[Monster],
        k: int,
        effect_type: EffectType,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with most effects of a type.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (
                    lambda entity: -sum(
                        1 for effect in entity.effects if effect.type == effect_type
                    )
                ),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )

    def _get_targets_least_effects(
        self,
        monsters: List[Monster],
        k: int,
        effect_type: EffectType,
        whitelist: List[Monster] = None,
        blacklist: List[Monster] = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
        ignore_immune_to: List[Keyword] = None,
        life_state: LifeState = LifeState.ALIVE,
        hurt: bool = False,
        consider: List[Keyword] = None,
    ) -> List[Monster]:
        """
        Returns k monsters with least effects of a type.
        """
        return filter_monsters(
            monsters,
            k=k,
            sort_functions=[
                (
                    lambda entity: sum(
                        1 for effect in entity.effects if effect.type == effect_type
                    )
                ),
            ],
            whitelist=whitelist,
            blacklist=blacklist,
            keyword_whitelist=keyword_whitelist,
            keyword_blacklist=keyword_blacklist,
            ignore_immune_to=ignore_immune_to,
            life_state=life_state,
            hurt=hurt,
            consider=consider,
            method="FIRST",
        )
