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

    Makes the target unable to act.
    """

    def __init__(
        self,
        duration: int = 2,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            keyword=Keyword.SLEEP,
            type=EffectType.DEBUFF,
            duration=duration,
            accuracy=accuracy,
            persistent=True,
            removable=removable,
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
