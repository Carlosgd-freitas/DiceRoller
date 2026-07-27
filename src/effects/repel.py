"""Repel effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class RepelEffect(Effect):
    """
    Repel Effect.

    Decreases the pririority of the target for enemies.
    """

    def __init__(
        self,
        duration: int = 2,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            keyword=Keyword.REPEL,
            type=EffectType.BUFF,
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
        removed_effects = []

        taunt = target.remove_effect(Keyword.TAUNT)
        if taunt:
            removed_effects.append(taunt)

        return {
            "removed_effects": removed_effects,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        return {}
