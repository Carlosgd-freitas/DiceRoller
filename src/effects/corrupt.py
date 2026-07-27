"""Corrupt effect module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class CorruptEffect(Effect):
    """
    Corrupt Effect.

    Removes buffs from the target, starting from the oldest.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        accuracy: float = 1,
    ):
        if value is None:
            value = Stat(flat=0)
        if min_value is None:
            min_value = Stat(flat=0)
        if max_value is None:
            max_value = Stat(flat=inf)

        super().__init__(
            keyword=Keyword.CORRUPT,
            type=EffectType.DETERIORATION,
            value=value,
            min_value=min_value,
            max_value=max_value,
            accuracy=accuracy,
            persistent=False,
        )

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
        removed_effects = []

        removed_effects = [
            effect
            for effect in target.effects
            if (effect.type == EffectType.BUFF) and (effect.removable)
        ]
        if self.value != inf:
            removed_effects = removed_effects[: self.value.flat]

        for buff in removed_effects:
            target.effects.remove(buff)

        target.equalize_stats()

        return {
            "removed_effects": removed_effects,
        }
