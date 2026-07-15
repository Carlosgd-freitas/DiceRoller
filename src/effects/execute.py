"""Execute effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class ExecuteEffect(Effect):
    """
    Execute Effect.

    Kills the target if it has hp less than or equal to (value_percent * 100)% of it's max HP.
    """

    def __init__(
        self,
        value: float = 0,
        value_percent: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.EXECUTE,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.DETERIORATION,
            persistent=False,
            removable=removable,
            target_keywords=target_keywords,
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
            threshold_0 = self.value or 0
            threshold_1 = (self.value_percent or 0) * target.max_hp
            threshold = max(threshold_0, threshold_1)

            if target.hp <= threshold:
                target.hp = 0
            else:
                fail = "default"
        else:
            fail = "dead"

        return {
            "fail": fail,
        }
