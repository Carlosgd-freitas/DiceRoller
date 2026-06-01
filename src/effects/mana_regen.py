"""Mana regen effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger

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
        duration: int = 1,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.MANA_REGEN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.BUFF,
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
        if target.hp > 0:
            target.mana += self.value

        return {
            "attribute": "mana",
        }
