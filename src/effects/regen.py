"""Regen effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.entity import Entity


class RegenEffect(Effect):
    """
    Regen Effect.

    Will increase the target's HP by the effect value at the start of each of the
    target's turn.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.REGEN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.RESTORATION,
            Trigger.TURN_START,
        )

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> None:
        return

    def activate(
        self,
        source: Entity,
        target: Entity,
    ) -> None:
        if target.hp > 0:
            target.hp += self.value
        target.equalize_stats()

        return
