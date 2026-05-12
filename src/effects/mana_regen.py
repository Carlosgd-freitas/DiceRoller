"""Mana regen effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.triggers import Trigger
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType

if TYPE_CHECKING:
    from src.base.entity import Entity


class ManaRegenEffect(Effect):
    """
    Mana Regen Effect.

    Will increase the target's mana by the effect value at the start of each of the 
    arget's turn.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.MANA_REGEN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.RESTORATION,
            Trigger.TURN_START,
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
        target.mana += self.value

        return
