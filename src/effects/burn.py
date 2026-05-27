"""Burn effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class BurnEffect(Effect):
    """
    Burn Effect.

    This is a debuff which will reduce the target's HP by the effect value at the start
    of each of the target's turn. Removes Freeze when applied.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.BURN,
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
    ) -> Dict:
        target.remove_effect(Keyword.FREEZE)
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> Dict:
        damage = calculate_damage(
            self,
            source,
            target,
        )

        target.hp -= damage
        target.equalize_stats()

        return {
            "damage": damage,
        }
