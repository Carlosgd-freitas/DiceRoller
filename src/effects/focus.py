"""Focus effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.entity import Entity


class FocusEffect(Effect):
    """
    Focus Effect.

    Buff that increases the target's accuracies. Removes Blind when applied.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 1,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.FOCUS,
            value,
            duration,
            decay,
            accuracy,
            EffectType.BUFF,
            None,
            True,
        )

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        fail = None
        removed_effects = []

        if target.is_alive():
            blind = target.remove_effect(Keyword.BLIND)
            if blind:
                removed_effects.append(blind)

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
        fail = None
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }
