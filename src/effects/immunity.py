"""Immunity effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class ImmunityEffect(Effect):
    """
    Immunity Effect.

    Makes the target immune to other effects.
    """

    def __init__(
        self,
        effects: List[Keyword] = None,
        value: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            Keyword.IMMUNITY,
            value,
            duration,
            decay,
            accuracy,
            EffectType.BUFF,
            None,
            True,
            removable,
        )
        self.effects = [] if effects is None else effects

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
