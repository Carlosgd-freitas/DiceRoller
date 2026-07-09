"""Selector module."""

from abc import ABC, abstractmethod
from typing import List

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.base.monster import LifeState, Monster
from src.systems.targeting.filters import filter_monsters


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
        main_keyword: Keyword,
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

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

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
        main_keyword: Keyword,
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

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

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
        main_keyword: Keyword,
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

        :param main_keyword: The main keyword of an Effect.
        :type main_keyword: Keyword

        :return: A list of target monsters.
        :rtype: List[Monster]
        """
        raise NotImplementedError

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
    ):
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
    ):
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
    ):
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
    ):
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
    ):
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
    ):
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
    ):
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

    def _preprocess_enemies(
        self,
        monsters: List[Monster],
    ) -> List[Monster]:
        """
        Preprocesses a list of enemy monsters for future targeting.
        """
        monsters = [
            monster for monster in monsters if not monster.get_effect(Keyword.INVISIBLE)
        ]

        return monsters
