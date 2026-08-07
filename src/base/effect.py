"""Effect module."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, List, TypedDict

from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.damage import DefendedDamage
    from src.base.entity import Entity
    from src.base.stat import Stat


class EffectData(TypedDict):
    """
    Data when applying or activating an Effect.

    :var damage: Damage done to a Monster.
    :vartype damage: int

    :var defended_damage: Defended damage data.
    :vartype defended_damage: DefendedDamage

    :var fail: The cause of the effect failing.
    :vartype fail: str

    :var healed: Healing done to a Monster.
    :vartype healed: int

    :var removed_effects: A list of effects that were removed.
    :vartype removed_effects: List[Effect]
    """

    damage: int
    defended_damage: DefendedDamage
    fail: str
    healed: int
    removed_effects: List[Effect]


class EffectRequirements(TypedDict):
    """
    Data containing requirements for executing an Effect.

    :var source_life_state: Life state required by the source monster.
    :vartype source_life_state: LifeState

    :var target_life_state: Life state required by the target monster.
    :vartype target_life_state: LifeState
    """

    source_life_state: LifeState
    target_life_state: LifeState


class EffectType(Enum):
    """Type of Effect."""

    ALL = "ALL"
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

    :var keyword: Effect keyword, which acts as an identifier.
    :vartype keyword: Keyword

    :var type: Effect type.
    :vartype type: EffectType

    :var value: Effect value.
    :vartype value: Stat | None

    :var min_value: Minimum threshold for Effect value.
    :vartype min_value: Stat | None

    :var max_value: Maximum threshold for Effect value.
    :vartype max_value: Stat | None

    :var duration: Effect duration in turns, in relation to the Entity the Effect
    will be applied to.
    :vartype duration: int | None

    :var delta: Increases or decreases Effect value at each turn end.
    :vartype delta: Stat | None

    :var accuracy: Effect chance of being applied in percentage format, usually
    inside [0, 1] interval. Default value is 1 (100%).
    :vartype accuracy: float

    :var trigger: Effect triggering condition.
    :vartype trigger: Trigger | None

    :var persistent: If the Effect is persistent or instant. Default value is False,
    meaning the Effect is instant.
    :vartype persistent: bool

    :var removable: If the Effect is removable by other Effects. Default value is True.
    :vartype removable: bool

    var target_keywords: What others keywords the Effect targets on its execution.
    :vartype target_keywords: List[Keyword] | None
    """

    def __init__(
        self,
        keyword: Keyword,
        type: EffectType,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        duration: int | None = None,
        delta: Stat | None = None,
        accuracy: float = 1,
        trigger: Trigger | None = None,
        persistent: bool = False,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        self.keyword = keyword
        self.type = type
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.duration = duration
        self.delta = delta
        self.accuracy = accuracy
        self.trigger = trigger
        self.persistent = persistent
        self.removable = removable
        self.target_keywords = target_keywords

    def __str__(self) -> str:
        """String representation of Effect."""
        trigger = self.trigger.value if self.trigger else None
        on_execute = "Persistent" if self.persistent else "Instant"

        if isinstance(self.target_keywords, list) and len(self.target_keywords) > 0:
            target_keywords = ", ".join(
                [str(keyword) for keyword in self.target_keywords]
            )
        else:
            target_keywords = str(self.target_keywords)

        _str = f"{self.keyword}"
        _str += f" | Type: {self.type.value}"
        _str += f" | Value: {str(self.value)}"
        _str += f" | Min Value: {str(self.min_value)}"
        _str += f" | Max Value: {str(self.max_value)}"
        _str += f" | Duration: {self.duration}"
        _str += f" | Delta: {str(self.delta)}"
        _str += f" | Acc: {self.accuracy * 100}%"
        _str += f" | Trigger: {trigger}"
        _str += f" | {on_execute}"
        _str += f" | Removable: {self.removable}"
        _str += f" | Target Keywords: {target_keywords}"

        return _str

    def get_requirements(self) -> EffectRequirements:
        """
        Returns the requirements for executing the Effect.

        :return: Effect requirements.
        :rtype: EffectRequirements
        """
        return {
            "source_life_state": LifeState.ALIVE,
            "target_life_state": LifeState.ALIVE,
        }

    def get_effective_value(
        self,
        source: Entity = None,
        target: Entity = None,
    ) -> float | None:
        """
        Returns the Effect effective value, that will be used in calculations and the
        effect execution.

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :return: The effective value.
        :rtype: float
        """
        # Base Value
        if self.value is None:
            return None
        elif self.value.flat is not None:
            effective_value = self.value.flat
        elif self.value.percent is not None:
            effective_value = self.value.percent
        else:
            return None

        # Clamping
        if (
            self.min_value
            and self.min_value.flat
            and effective_value < self.min_value.flat
        ):
            effective_value = self.min_value.flat

        if (
            self.max_value
            and self.max_value.flat
            and effective_value > self.max_value.flat
        ):
            effective_value = self.max_value.flat

        return effective_value

    def get_valid_target_keywords(self) -> List[Keyword]:
        """
        Returns a list containing the valid targt keywords for the Effect.

        :return: Valid targt keywords for the Effect.
        :rtype: List[Keyword]
        """
        return None

    def get_description_variable_key(self) -> str:
        """
        Returns a message key for the Effect description that takes the parameters into
        consideration.

        :return: The message key.
        :rtype: str
        """
        return "description_variable"

    def stack(
        self,
        new_effect: Effect,
    ):
        """
        Modifies the Effect parameters based on a new effect, if both are of the same
        class:
        * value of both effects are summed.
        * the lowest min value between the two effects is maintained.
        * the highest max value between the two effects is maintained.
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

        # Value
        if self.value is not None and new_effect.value is not None:
            self.value.add(new_effect.value, "flat")
            self.value.add(new_effect.value, "percent")

        # Min Value
        if self.min_value is not None and new_effect.min_value is not None:
            self.min_value.lowest(new_effect.min_value, "flat")
            self.min_value.lowest(new_effect.min_value, "percent")

        # Max Value
        if self.max_value is not None and new_effect.max_value is not None:
            self.max_value.highest(new_effect.max_value, "flat")
            self.max_value.highest(new_effect.max_value, "percent")

        # Duration
        if (
            self.duration is not None
            and new_effect.duration is not None
            and new_effect.duration > self.duration
        ):
            self.duration = new_effect.duration

        # Delta
        if self.delta is not None and new_effect.delta is not None:
            self.delta.add(new_effect.delta, "flat")
            self.delta.add(new_effect.delta, "percent")

        # Accuracy
        if new_effect.accuracy > self.accuracy:
            self.accuracy = new_effect.accuracy

        # Removable
        if not new_effect.removable:
            self.removable = False

        # Target Keywords
        if isinstance(self.target_keywords, list) and isinstance(
            new_effect.target_keywords, list
        ):
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

    def is_equivalent(self, effect: Effect) -> bool:
        """
        Compares two effects and returns if they are equivalent.

        :param effect: Effect for comparison.
        :type effect: Effect

        :return: If the effects are equivalent.
        :rtype: bool
        """
        return (
            isinstance(effect, Effect)
            and self.keyword == effect.keyword
            and self.value == effect.value
            and self.removable == effect.removable
            and self.target_keywords == effect.target_keywords
        )
