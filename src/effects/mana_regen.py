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

    If the target is alive, increases its mana by the effect value at the start of each
    of the target's turn.
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
        fail = None
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        fail = None

        if target.is_alive():
            target.mana += self.value
        else:
            fail = "dead"

        return {
            "attribute": "mana",
            "fail": fail,
        }
