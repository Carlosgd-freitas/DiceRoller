"""Sleep effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class SleepEffect(Effect):
    """
    Sleep Effect.

    This is a debuff which will make the target unable to roll dice, use items or
    active skills.
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
            Keyword.SLEEP,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
            None,
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
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }
