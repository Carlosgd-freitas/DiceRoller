"""Cleanse effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class CleanseEffect(Effect):
    """
    Cleanse Effect.

    Removes debuffs from the target, starting from the oldest.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            Keyword.CLEANSE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.RESTORATION,
            None,
            False,
            removable,
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
        fail = None
        removed_effects = []

        if target.is_alive():

            removed_effects = [
                effect
                for effect in target.effects
                if (effect.type == EffectType.DEBUFF) and (effect.removable)
            ][: self.value]

            for debuff in removed_effects:
                target.effects.remove(debuff)

            target.equalize_stats()

        else:
            fail = "dead"

        return {
            "fail": fail,
            "removed_effects": removed_effects,
        }
