"""Curse effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType

if TYPE_CHECKING:
    from src.base.entity import Entity


class CurseEffect(Effect):
    """
    Curse Effect.

    Will reduce the target's HP by the effect value.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.CURSE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.OFFENSIVE,
        )

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        target.hp -= self.value
        target.equalize_stats()

        return
