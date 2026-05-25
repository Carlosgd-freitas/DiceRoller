"""Block effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class BlockEffect(Effect):
    """
    Block Effect.

    This will reduce direct damage done to the target's HP.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.BLOCK,
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
    ) -> None:
        return

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> None:
        return
