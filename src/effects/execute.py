"""Execute effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class ExecuteEffect(Effect):
    """
    Execute Effect.

    Kills the target if it has hp less than or equal to (value * 100)% of it's max HP.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.EXECUTE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DETERIORATION,
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
        fail = None

        if target.is_alive():
            if target.hp <= (target.max_hp * self.value):
                target.hp = 0
            else:
                fail = "default"
        else:
            fail = "dead"

        return {
            "fail": fail,
        }
