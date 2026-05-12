"""Drain effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class DrainEffect(Effect):
    """
    Drain Effect.

    Will reduce the target's HP by the effect value, while increasing the source's HP.
    The damage done will be affected by the target's Block.
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

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        damage = calculate_damage(
            self,
            source,
            target,
            consider_block=True
        )

        target.hp -= damage
        target.equalize_stats()

        source.hp += damage
        source.equalize_stats()

        return
