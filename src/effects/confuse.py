"""Confuse effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class ConfuseEffect(Effect):
    """
    Confuse Effect.

    This is a debuff which makes the target to target randomly when using dice or
    skills.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.CONFUSE,
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
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> Dict:
        return {}
