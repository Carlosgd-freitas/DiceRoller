"""Revive effect module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class ReviveEffect(Effect):
    """
    Revive Effect.

    Increases the target's HP by (value * 100)% of it's max HP, rounding up, but only
    if it is dead.
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
            Keyword.REVIVE,
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

        if not target.is_alive():
            if target.in_combat:
                target.in_combat = True
            target.hp += ceil(target.max_hp * self.value)
            target.equalize_stats()
        else:
            fail = "alive"

        return {
            "attribute": "hp",
            "fail": fail,
        }
