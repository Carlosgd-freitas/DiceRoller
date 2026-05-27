"""Drain effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class DrainEffect(Effect):
    """
    Drain Effect.

    Will reduce the target's HP by the effect value, while increasing the source's HP
    and remove Sleep from it. The damage done will be affected by the target's Block.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.DRAIN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.OFFENSIVE,
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
        target.remove_effect(Keyword.SLEEP)

        damage = calculate_damage(self, source, target, consider_block=True)

        target.hp -= damage
        target.equalize_stats()

        source.hp += damage
        source.equalize_stats()

        return {
            "damage": damage,
        }
