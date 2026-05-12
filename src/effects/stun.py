"""Stun effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword
from src.base.effect import Effect, EffectType

if TYPE_CHECKING:
    from src.base.entity import Entity


class StunEffect(Effect):
    """
    Stun Effect.

    This is a debuff which will make the target unable to roll dice, use items or
    active skills.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
    ):
        super().__init__(
            Keyword.STUN,
            value,
            duration,
            decay,
            accuracy,
            EffectType.DEBUFF,
        )

    def activate(
        self,
        source: "Entity",
        target: "Entity",
    ) -> None:
        return
