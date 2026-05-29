"""Thorns effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class ThornsEffect(Effect):
    """
    Thorns Effect.

    When the target is attacked, the monster who attacked it will have their HP reduced
    by the effect value.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.THORNS,
            value,
            duration,
            decay,
            accuracy,
            EffectType.BUFF,
            Trigger.BEING_ATTACKED,
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
        damage = calculate_damage(self, source, target, consider_block=True)

        target.hp -= damage
        target.equalize_stats()

        return {
            "damage": damage,
        }
