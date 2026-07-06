"""Block effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
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
        value_percent: float = 0,
        duration: int = 2,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.BLOCK,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.DEFENSIVE,
            persistent=True,
            removable=removable,
            target_keywords=target_keywords,
        )

    def get_effective_value(
        self,
        source: Entity,
        target: Entity,
    ) -> float:
        """
        Returns the effects' effective value, taking effects on source and target
        entities into account.

        :return: The effective value.
        :rtype: float
        """
        effective_value = self.value

        if source:
            fortify = source.get_effect(Keyword.FORTIFY)
            if fortify:
                effective_value += fortify.value

            fragile = source.get_effect(Keyword.FRAGILE)
            if fragile:
                effective_value -= fragile.value

        if effective_value < 0:
            effective_value = 0

        return effective_value

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
        return {}
