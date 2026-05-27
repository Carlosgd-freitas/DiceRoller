"""Freeze effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class FreezeEffect(Effect):
    """
    Freeze Effect.

    This is a debuff which will make the target unable to roll dice, use items or
    active skills. Removes Burn when applied.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.FREEZE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
            None,
            True,
        )

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> Dict:
        target.remove_effect(Keyword.BURN)
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> Dict:
        return {}
