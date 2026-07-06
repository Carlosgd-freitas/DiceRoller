"""Confuse effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
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
        value_percent: float = 0,
        duration: int = 1,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.CONFUSE,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.DEBUFF,
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
