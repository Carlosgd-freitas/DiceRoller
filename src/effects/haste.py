"""Haste effect module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class HasteEffect(Effect):
    """
    Haste Effect.

    Increases target's speed.
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
        if value is None:
            value = Stat(flat=0, percent=0)
        if min_value is None:
            min_value = Stat(flat=0, percent=0)
        if max_value is None:
            max_value = Stat(flat=inf, percent=inf)

        super().__init__(
            keyword=Keyword.HASTE,
            type=EffectType.BUFF,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
            accuracy=accuracy,
            persistent=True,
            removable=removable,
        )

    def get_description_variable_key(self) -> str:
        """
        Returns a message key for the Effect description that takes the parameters into
        consideration.

        :return: The message key.
        :rtype: str
        """
        if (not self.value.flat) and (not self.value.percent):
            return "description_flat"
        elif (self.value.flat) and (not self.value.percent):
            return "description_flat"
        elif (not self.value.flat) and (self.value.percent):
            return "description_percent"
        else:
            return "description_both"

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        removed_effects = []

        slow = target.remove_effect(Keyword.SLOW)
        if slow:
            removed_effects.append(slow)

        return {
            "removed_effects": removed_effects,
        }

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        return {}
