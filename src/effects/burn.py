"""Burn effect module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class BurnEffect(Effect):
    """
    Burn Effect.

    Reduces the target HP each turn start and removes Freeze.
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
        if min_value is None:
            min_value = Stat(percent=0)

        super().__init__(
            keyword=Keyword.BURN,
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
    ) -> float:
        """
        Returns the effects' effective value, taking effects on source and target
        entities into account.

        :return: The effective value.
        :rtype: float
        """
        if self.value.flat is None and self.value.percent is None:
            return None

        # Base Value
        effective_value = 0

        if self.value.flat is not None:
            effective_value += self.value.flat
        if self.value.percent is not None:
            effective_value += self.value.percent * target.max_hp

        # Modifiers
        if target:
            # Oil
            oil = target.get_effect(Keyword.OIL)
            if oil:

                if oil.value.flat:
                    effective_value += oil.value.flat
                if oil.value.percent:
                    effective_value += effective_value * oil.value.percent

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

        return ceil(effective_value)

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        fail = None
        removed_effects = []

        if target.is_alive():
            freeze = target.remove_effect(Keyword.FREEZE)
            if freeze:
                removed_effects.append(freeze)

        else:
            fail = "dead"

        return {
            "fail": fail,
            "removed_effects": removed_effects,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        damage_data = {}
        fail = None

        if target.is_alive():
            damage_data = calculate_damage(
                self,
                source,
                target,
            )

            target.hp -= damage_data["damage"]
            target.equalize_stats()

        else:
            fail = "dead"

        return {
            **damage_data,
            "fail": fail,
        }
