"""Selector module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Literal

from src.targeting.filters import filter_entities

if TYPE_CHECKING:
    from src.base.keywords import Keyword
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
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k random monsters.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="RANDOM",
            life_state=life_state,
            exclude=exclude,
        )

    def _get_targets_highest_hp(
        self,
        monsters: List[Monster],
        k: int,
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k monsters with most effective hp and hp.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="FIRST",
            sort_functions=[
                (lambda entity: -entity.get_effective_hp()),
                (lambda entity: -entity.hp),
            ],
            life_state=life_state,
            exclude=exclude,
        )

    def _get_targets_lowest_hp(
        self,
        monsters: List[Monster],
        k: int,
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k monsters with least effective hp and hp.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="FIRST",
            sort_functions=[
                (lambda entity: entity.get_effective_hp()),
                (lambda entity: entity.hp),
            ],
            life_state=life_state,
            exclude=exclude,
        )

    def _get_targets_highest_max_hp(
        self,
        monsters: List[Monster],
        k: int,
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k monsters with most max hp.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="FIRST",
            sort_functions=[
                (lambda entity: -entity.max_hp),
            ],
            life_state=life_state,
            exclude=exclude,
        )

    def _get_targets_lowest_max_hp(
        self,
        monsters: List[Monster],
        k: int,
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k monsters with least max hp.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="FIRST",
            sort_functions=[
                (lambda entity: entity.max_hp),
            ],
            life_state=life_state,
            exclude=exclude,
        )

    def _get_targets_with_effects(
        self,
        monsters: List[Monster],
        k: int,
        effects: List[Keyword],
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k random monsters with effects.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="RANDOM",
            life_state=life_state,
            keyword_whitelist=effects,
            exclude=exclude,
        )

    def _get_targets_without_effects(
        self,
        monsters: List[Monster],
        k: int,
        effects: List[Keyword],
        life_state: Literal["ALIVE", "DEAD", "ANY"] = "ALIVE",
        exclude: List[str] = None,
    ):
        """
        Returns k random monsters without effects.
        """
        exclude = [] if exclude is None else exclude
        return filter_entities(
            monsters,
            k=k,
            method="RANDOM",
            life_state=life_state,
            keyword_blacklist=effects,
            exclude=exclude,
        )
