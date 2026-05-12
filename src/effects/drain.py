"""Drain effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType

if TYPE_CHECKING:
    from src.base.entity import Entity


class DrainEffect(Effect):
    """
    Drain Effect.

    Will reduce the target's HP by the effect value, while increasing the source's HP.
    The damage done will be affected by the target's Block.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.DRAIN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.OFFENSIVE,
        )

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        damage = self.value
        blocking = target.get_effect(Keyword.BLOCK)

        if blocking:
            min_value = min(damage, blocking.value)

            damage -= min_value
            blocking.value -= min_value

            if blocking.value <= 0:
                target.effects.remove(blocking)

        if damage < 0:
            damage = 0

        target.hp -= damage
        target.equalize_stats()

        source.hp += damage
        source.equalize_stats()

        return
