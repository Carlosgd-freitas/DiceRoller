"""Invulnerable effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class InvulnerableEffect(Effect):
    """
    Invulnerable Effect.

    Negates any damage done to the target.
    """

    def __init__(
        self,
        duration: int = 2,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            keyword=Keyword.INVULNERABLE,
            type=EffectType.DEFENSIVE,
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
