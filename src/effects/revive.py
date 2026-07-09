"""Revive effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.processors.healing import calculate_healing

if TYPE_CHECKING:
    from src.base.entity import Entity


class ReviveEffect(Effect):
    """
    Revive Effect.

    If the target is dead, returns it to combat and heals its HP by value and
    (value_percent * 100) of its max HP, rounding up.
    """

    def __init__(
        self,
        value: float = 0,
        value_percent: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        super().__init__(
            keyword=Keyword.REVIVE,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.RESTORATION,
            persistent=False,
            removable=removable,
            target_keywords=target_keywords,
        )

    def affects(self) -> LifeState:
        """
        Returns the life state of monsters that this effect can target.

        :return: The required target life state.
        :rtype: LifeState
        """
        return LifeState.DEAD

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        return {}

    def activate(
        self,
        target: Entity,
        source: Entity | None = None,
    ) -> EffectData:
        fail = None
        healed = None

        if not target.is_alive():
            if target.in_combat:
                target.in_combat = True

            healed = calculate_healing(
                self,
                source,
                target,
            )

            target.hp += healed
            target.equalize_stats()

        else:
            fail = "alive"

        return {
            "fail": fail,
            "healed": healed,
        }
