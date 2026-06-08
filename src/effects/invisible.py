"""Invisible effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class InvisibleEffect(Effect):
    """
    Invisible Effect.

    This will avoid any direct damage that would be done to the target's HP.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.INVISIBLE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEFENSIVE,
            None,
            True,
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
        return {}
