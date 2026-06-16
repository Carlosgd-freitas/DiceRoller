"""Doom effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.entity import Entity


class DoomEffect(Effect):
    """
    Doom Effect.

    Kills the target at turn end if expiring.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 1,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            Keyword.DOOM,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
            Trigger.DURATION_DECAY,
            True,
            removable,
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

        if (target.is_alive()) and (self.duration == 0):
            target.hp = 0
        else:
            fail = "dead"

        return {
            "fail": fail,
        }
