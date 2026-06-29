"""Slow effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class SlowEffect(Effect):
    """
    Slow Effect.

    Decreases target's speed.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            Keyword.SLOW,
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
        removed_effects = []

        if target.is_alive():
            haste = target.remove_effect(Keyword.HASTE)
            if haste:
                removed_effects.append(haste)

        else:
            fail = "dead"

        return {
            "fail": fail,
            "removed_effects": removed_effects,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        return {}
