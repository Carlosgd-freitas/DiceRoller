"""Poison effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class PoisonEffect(Effect):
    """
    Poison Effect.

    This is a debuff which will reduce the target's HP by the effect value at the start
    of each of the target's turn.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.POISON,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
            Trigger.TURN_START,
            True,
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
        damage_data = calculate_damage(
            self,
            source,
            target,
        )

        target.hp -= damage_data["damage"]
        target.equalize_stats()

        return damage_data
