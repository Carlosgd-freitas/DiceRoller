"""Heal effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class HealEffect(Effect):
    """
    Heal Effect.

    Will increase the target's HP by the effect value.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.HEAL,
            value,
            duration,
            decay,
            accuracy,
            EffectType.RESTORATION,
        )

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> Dict:
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> Dict:
        if target.hp > 0:
            target.hp += self.value
        target.equalize_stats()

        return {
            "attribute": "hp",
        }
