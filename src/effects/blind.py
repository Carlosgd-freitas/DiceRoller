"""Blind effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class BlindEffect(Effect):
    """
    Blind Effect.

    Decreases the target's accuracies when it targets something other then themselves.
    Removes Focus.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        duration: int = 2,
        delta: Stat | None = None,
        accuracy: float = 1,
        removable: bool = True,
    ):
        if min_value is None:
            min_value = Stat(percent=0)

        super().__init__(
            keyword=Keyword.BLIND,
            type=EffectType.DEBUFF,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
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
        removed_effects = []

        if target.is_alive():
            focus = target.remove_effect(Keyword.FOCUS)
            if focus:
                removed_effects.append(focus)

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
