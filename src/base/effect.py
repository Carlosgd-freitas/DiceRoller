"""Effect module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List, TypedDict

from src.base.keywords import Keyword
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
    CURSE = "CURSE"
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

    :var value_percent: Effect's value in percentage format, usually inside [0, 1]
    interval. Default value is 0 (0%).
    :vartype value_percent: float

    :var duration: Effect's duration in turns, in relation to the Entity the Effect
    will be applied to. Default value is 0.
    :vartype duration: int

    :var decay: Effect's value decay for each turn. A negative decay will increase the
    Effect's value instead. Default value is 0.
    :vartype decay: float

    :var accuracy: Effect's chance of being applied in percentage format, usually
    inside [0, 1] interval. Default value is 1 (100%).
    :vartype accuracy: float

    :var type: Effect's type.
    :vartype type: EffectType

    :var trigger: Effect's triggering condition.
    :vartype trigger: Trigger

    :var persistent: If the Effect is persistent or instant. Default value is False.
    :vartype persistent: bool

    :var removable: If the Effect is removable by other Effects. Default value is True.
    :vartype removable: bool

    var removable: If the Effect is removable by other Effects. Default value is True.
    :vartype removable: bool

    var target_keywords: What others keywords the Effect targets on its execution.
    Default value is an empty list.
    :vartype target_keywords: List[Keyword]
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = 0,
        value_percent: float = 0,
        duration: float = 0,
        decay: float = 0,
        accuracy: float = 1,
        type: EffectType = None,
        trigger: Trigger = None,
        persistent: bool = False,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        self.keyword = keyword
        self.value = value
        self.value_percent = value_percent
        self.duration = duration
        self.decay = decay
        self.accuracy = accuracy
        self.type = type
        self.trigger = trigger
        self.persistent = persistent
        self.removable = removable
        self.target_keywords = [] if target_keywords is None else target_keywords

    def __str__(self) -> str:
        """String representation of Effect."""
        type = self.type.value if self.type else None
        trigger = self.trigger.value if self.trigger else None
        target_keywords = ", ".join([str(keyword) for keyword in self.target_keywords])

        _str = f"{self.keyword}"
        _str += f" | Value: {self.value}"
        _str += f" | Value (%): {self.value_percent}"
        _str += f" | Duration: {self.duration}"
        _str += f" | Decay: {self.decay}"
        _str += f" | Acc (%): {self.accuracy}"
        _str += f" | Type: {type}"
        _str += f" | Trigger: {trigger}"
        _str += f" | Persistent: {self.persistent}"
        _str += f" | Removable: {self.removable}"
        _str += f" | Target Keywords: {target_keywords}"

        return _str

    def get_effective_value(
        self,
        source: Entity = None,
        target: Entity = None,
    ) -> float:
        """
        Returns the effects' effective value, taking effects on source and target
        entities into account.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :return: The effective value.
        :rtype: float
        """
        return self.value

    def get_effective_value_percent(
        self,
        source: Entity = None,
        target: Entity = None,
    ) -> float:
        """
        Returns the effects' effective value percent, taking effects on source and
        target entities into account.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :return: The effective value percent.
        :rtype: float
        """
        return self.value_percent

    def stack(
        self,
        new_effect: Effect,
    ):
        """
        Modifies the Effect parameters based on a new effect, if both are of the same
        class:
        * value of both effects are summed.
        * value (percentage) of both effects are summed.
        * the highest duration between the two effects is maintained.
        * decay of both effects are summed.
        * the highest accuracy between the two effects is maintained.
        * if the new effect is not removable, then the stacked effect will be also.
        * any target keywords from the new effect that aren't in the Effect will be added.

        :param new_effect: A new effect that is being applied to an Entity.
        :type new_effect: Effect
        """
        if type(self) is not type(new_effect):
            return

        self.value += new_effect.value
        self.value_percent += new_effect.value_percent

        if new_effect.duration > self.duration:
            self.duration = new_effect.duration

        self.decay += new_effect.decay

        if new_effect.accuracy > self.accuracy:
            self.accuracy = new_effect.accuracy

        if not new_effect.removable:
            self.removable = False

        for new_target_keyword in new_effect.target_keywords:
            if new_target_keyword not in self.target_keywords:
                self.target_keywords.append(new_target_keyword)

        return

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
