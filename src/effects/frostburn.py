"""Frostburn effect module."""

from __future__ import annotations

from math import ceil, inf
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class FrostburnEffect(Effect):
    """
    Frostburn Effect.

    Reduces the target HP each turn start.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        duration: int = 2,
        delta: Stat | None = None,
        accuracy: float = 1,
        removable: bool = True,
    ):
        if value is None:
            value = Stat(flat=0, percent=0)
        if min_value is None:
            min_value = Stat(flat=0, percent=0)
        if max_value is None:
            max_value = Stat(flat=inf, percent=inf)

        super().__init__(
            keyword=Keyword.FROSTBURN,
            type=EffectType.DEBUFF,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
            accuracy=accuracy,
            trigger=Trigger.TURN_START,
            persistent=True,
            removable=removable,
        )

    def get_effective_value(
        self,
        source: Entity,
        target: Entity,
    ) -> Stat:
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
        if self.value.flat is None and self.value.percent is None:
            return None

        # Base Value
        effective_value = 0

        if self.value.flat is not None:
            effective_value += self.value.flat
        if (self.value.percent is not None) and (target is not None):
            effective_value += self.value.percent * target.max_hp

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

        if (effective_value != inf) and (effective_value != -inf):
            effective_value = ceil(effective_value)

        return effective_value

    def get_description_variable_key(self) -> str:
        """
        Returns a message key for the Effect description that takes the parameters into
        consideration.

        :return: The message key.
        :rtype: str
        """
        if (not self.value.flat) and (not self.value.percent):
            return "description_flat"
        elif (self.value.flat) and (not self.value.percent):
            return "description_flat"
        elif (not self.value.flat) and (self.value.percent):
            return "description_percent"
        else:
            return "description_both"

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        damage_data = calculate_damage(
            self,
            source,
            target,
        )

        target.hp -= damage_data["damage"]
        target.equalize_stats()

        return damage_data
