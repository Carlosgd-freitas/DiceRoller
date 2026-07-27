"""Sacred Block effect module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class SacredBlockEffect(Effect):
    """
    Sacred Block Effect.

    Negates direct damage done to the target a number of times equal to its value.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        duration: int = 2,
        delta: Stat | None = None,
        accuracy: float = 1,
        removable: bool = True,
    ):
        if value is None:
            value = Stat(flat=0)
        if min_value is None:
            min_value = Stat(flat=0)
        if max_value is None:
            max_value = Stat(flat=inf)

        super().__init__(
            keyword=Keyword.SACRED_BLOCK,
            type=EffectType.DEFENSIVE,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
            accuracy=accuracy,
            persistent=True,
            removable=removable,
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
        return {}
