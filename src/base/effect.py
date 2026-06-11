"""Effect module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List, TypedDict

from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.entity import Entity


class EffectData(TypedDict):
    """
    Data when applying or activating an Effect.

    :var absorbed_damage: Damage that was absorbed by a Monster.
    :vartype absorbed_damage: int

    :var attribute: Attribute of a Monster that was affected.
    :vartype attribute: str

    :var blocked_damage: Damage that was blocked by a Monster.
    :vartype blocked_damage: int

    :var damage: Damage done to a Monster.
    :vartype damage: int

    :var fail: The cause of the effect failing.
    :vartype fail: str

    :var removed_effects: A list of effects that were removed on effect apply.
    :vartype removed_effects: List[Effect]
    """

    absorbed_damage: int
    attribute: str
    blocked_damage: int
    damage: int
    fail: str
    removed_effects: List[Effect]


class EffectType(Enum):
    """Type of Effect."""

    BUFF = "BUFF"
    DEBUFF = "DEBUFF"
    DEFENSIVE = "DEFENSIVE"
    DETERIORATION = "DETERIORATION"
    NOTHING = "NOTHING"
    OFFENSIVE = "OFFENSIVE"
    RESTORATION = "RESTORATION"


class Effect(ABC):
    """
    Effect class.

    :var keyword: Effect's keyword.
    :vartype keyword: Keyword

    :var value: Effect's value. Default value is 0.
    :vartype value: float

    :var duration: Effect's duration in turns, in relation to the Entity the Effect
    will be applied to. Default value is 0.
    :vartype duration: int

    :var decay: Effect's value decay for each turn. A negative decay will increase the
    Effect's value instead. Default value is 0.
    :vartype decay: float

    :var accuracy: Effect's chance of being applied, in interval [0, 1]. Default value
    is 1 (100%).
    :vartype accuracy: float

    :var type: Effect's type.
    :vartype type: EffectType

    :var trigger: Effect's triggering condition.
    :vartype trigger: Trigger

    :var persistent: If the Effect is persistent or instant. Default value is False.
    :vartype persistent: bool

    :var removable: If the Effect is removable by other Effects. Default value is True.
    :vartype removable: bool
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        type: EffectType = None,
        trigger: Trigger = None,
        persistent: bool = False,
        removable: bool = True,
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.accuracy = accuracy
        self.type = type
        self.trigger = trigger
        self.persistent = persistent
        self.removable = removable

    def __str__(self) -> str:
        color_params = get_keyword_color(self.keyword)

        _str = color_string(
            string=self.keyword.value,
            foreground_color=color_params["foreground_color"],
            intensity=color_params["intensity"],
        )

        if self.value:
            _str += f" {self.value}"

        return _str

    @abstractmethod
    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        """
        What the Effect will do when being applied to an Entity.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :return: A dictionary containing data after the effect was applied.
        :rtype: Dict
        """
        raise NotImplementedError

    @abstractmethod
    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        """
        What the Effect will done when activated.

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :return: A dictionary containing data after the effect was activated.
        :rtype: Dict
        """
        raise NotImplementedError
