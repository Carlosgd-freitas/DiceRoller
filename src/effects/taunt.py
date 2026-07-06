"""Taunt effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class TauntEffect(Effect):
    """
    Taunt Effect.

    Increases the pririority of the target for enemies.
    """

    def __init__(
        self,
        value: float = 0,
        value_percent: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.TAUNT,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.BUFF,
            persistent=True,
            removable=removable,
            target_keywords=target_keywords,
        )

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        fail = None
        removed_effects = []

        if target.is_alive():
            repel = target.remove_effect(Keyword.REPEL)
            if repel:
                removed_effects.append(repel)

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
