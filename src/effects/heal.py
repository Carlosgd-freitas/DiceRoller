"""Heal effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType

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
        source: "Entity",
        target: "Entity",
    ) -> None:
        return

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        target.hp += self.value
        target.equalize_stats()

        return
