"""Absorb effect module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class AbsorbEffect(Effect):
    """
    Absorb Effect.

    Reduces direct damage done to the target by its value, while healing them by the
    damage reduced.
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
            min_value = Stat(flat=0, percent=0)

        super().__init__(
            keyword=Keyword.ABSORB,
            type=EffectType.DEFENSIVE,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
            accuracy=accuracy,
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
        if self.value.percent is not None:
            effective_value += self.value.percent * target.max_hp

        # Modifiers
        if source:
            # Fortify
            fortify = source.get_effect(Keyword.FORTIFY)
            if fortify:

                if fortify.value.flat:
                    effective_value += fortify.value.flat
                if fortify.value.percent:
                    effective_value += effective_value * fortify.value.percent

            # Fragile
            fragile = source.get_effect(Keyword.FRAGILE)
            if fragile:

                if fragile.value.flat:
                    effective_value -= fragile.value.flat
                if fragile.value.percent:
                    effective_value -= effective_value * fragile.value.percent

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

        if target.is_alive():
            self.value.flat = self.get_effective_value(source=source, target=target)
            self.value.percent = None

        else:
            fail = "dead"

        return {
            "fail": fail,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        fail = None
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }
