"""All effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class AllEffect(Effect):
    """
    All Effect.

    Considered as every other effect, but does nothing.
    """

    def __init__(self):
        super().__init__(
            keyword=Keyword.ALL,
            type=EffectType.ALL,
            persistent=False,
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
