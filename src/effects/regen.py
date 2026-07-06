"""Regen effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.processors.healing import calculate_healing

if TYPE_CHECKING:
    from src.base.entity import Entity


class RegenEffect(Effect):
    """
    Regen Effect.

    If the target is alive, increases its HP by the effect value at the start of each
    of the target's turn.
    """

    def __init__(
        self,
        value: float = 0,
        value_percent: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.REGEN,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.BUFF,
            trigger=Trigger.TURN_START,
            persistent=True,
            removable=removable,
            target_keywords=target_keywords,
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
        healed = None

        if target.is_alive():
            healed = calculate_healing(
                self,
                source,
                target,
            )

            target.hp += healed
            target.equalize_stats()

        else:
            fail = "dead"

        return {
            "fail": fail,
            "healed": healed,
        }
