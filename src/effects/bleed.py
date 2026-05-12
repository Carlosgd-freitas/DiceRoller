"""Bleed effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.triggers import Trigger
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class BleedEffect(Effect):
    """
    Bleed Effect.

    This is a debuff which will reduce the target's HP by the effect value after each
    of the target's dice is rolled.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.BLEED,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
            Trigger.ROLL,
        )

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        damage = calculate_damage(
            self,
            source,
            target,
        )

        target.hp -= damage
        target.equalize_stats()

        return
