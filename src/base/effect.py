"""Effect module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from src.base.keywords import Keyword, color_keyword
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.entity import Entity


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

    :var accuracy: Effect's chance of being applied, in interval [0, 1]. Default value is
    1 (100%).
    :vartype accuracy: float

    :var type: Effect's type. By default, this value will depend on keyword.
    :vartype type: EffectType

    :var trigger: Effect's triggering condition. By default, this value will depend on
    keyword.
    :vartype trigger: Trigger

    :var incompatible: Effect's incompatible keywords, which will be removed if this Effect
    is added to an Entity. By default, this value will depend on keyword.
    :vartype incompatible: List[Keyword]
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
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.accuracy = accuracy
        self.type = type
        self.trigger = trigger

    def __str__(self) -> str:
        _str = color_keyword(self.keyword)

        if self.value:
            _str += f" {self.value}"

        return _str

    @abstractmethod
    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> None:
        """
        What the Effect will do when being applied to an Entity.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity
        """
        raise NotImplementedError

    @abstractmethod
    def activate(
        self,
        source: Entity,
        target: Entity,
    ) -> None:
        """
        What the Effect will done when activated.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity
        """
        raise NotImplementedError
