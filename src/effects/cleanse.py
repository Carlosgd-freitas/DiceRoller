"""Cleanse effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class CleanseEffect(Effect):
    """
    Cleanse Effect.

    Removes debuffs from the target, starting from the oldest.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        accuracy: float = 1,
    ):
        if min_value is None:
            min_value = Stat(flat=0)

        super().__init__(
            keyword=Keyword.CLEANSE,
            type=EffectType.RESTORATION,
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
        fail = None
        removed_effects = []

        if target.is_alive():

            removed_effects = [
                effect
                for effect in target.effects
                if (effect.type == EffectType.DEBUFF) and (effect.removable)
            ][: self.value.flat]

            for debuff in removed_effects:
                target.effects.remove(debuff)

            target.equalize_stats()

        else:
            fail = "dead"

        return {
            "fail": fail,
            "removed_effects": removed_effects,
        }
