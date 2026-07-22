"""Attack effect module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class AttackEffect(Effect):
    """
    Attack Effect.

    Reduces the target HP and removes Sleep.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        accuracy: float = 1,
    ):
        if min_value is None:
            min_value = Stat(flat=0, percent=0)

        super().__init__(
            keyword=Keyword.ATTACK,
            type=EffectType.OFFENSIVE,
            value=value,
            min_value=min_value,
            max_value=max_value,
            accuracy=accuracy,
            persistent=False,
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
        if self.value.percent is not None:
            effective_value += self.value.percent * target.max_hp

        # Modifiers
        if source:
            # Strength
            strength = source.get_effect(Keyword.STRENGTH)
            if strength:

                if strength.value.flat:
                    effective_value += strength.value.flat
                if strength.value.percent:
                    effective_value += effective_value * strength.value.percent

            # Weak
            weak = source.get_effect(Keyword.WEAK)
            if weak:

                if weak.value.flat:
                    effective_value -= weak.value.flat
                if weak.value.percent:
                    effective_value -= effective_value * weak.value.percent

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
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        damage_data = {}
        fail = None
        removed_effects = []

        if target.is_alive():
            sleep = target.remove_effect(Keyword.SLEEP)
            if sleep:
                removed_effects.append(sleep)

            damage_data = calculate_damage(
                self,
                source,
                target,
                consider=[
                    Keyword.ABSORB,
                    Keyword.BLOCK,
                    Keyword.INVULNERABLE,
                    Keyword.SACRED_BLOCK,
                ],
            )

            target.hp -= damage_data["damage"]
            target.equalize_stats()

        else:
            fail = "dead"

        return {
            **damage_data,
            "fail": fail,
            "removed_effects": removed_effects,
        }
