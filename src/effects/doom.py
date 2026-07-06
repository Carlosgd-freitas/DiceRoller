"""Doom effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger

if TYPE_CHECKING:
    from src.base.entity import Entity


class DoomEffect(Effect):
    """
    Doom Effect.

    Kills the target at turn end if expiring.
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
            keyword=Keyword.DOOM,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.DEBUFF,
            trigger=Trigger.DURATION_DECAY,
            persistent=True,
            removable=removable,
            target_keywords=target_keywords,
        )

    def stack(
        self,
        new_effect: DoomEffect,
    ):
        """
        Modifies the DoomEffect parameters based on a new effect, if both are of the
        sameclass:
        * value of both effects are summed.
        * the lowest duration between the two effects is maintained.
        * decay of both effects are summed.
        * the highest accuracy between the two effects is maintained.
        * if the new effect is not removable, then the stacked effect will be also.

        :param new_effect: A new effect that is being applied to an Entity.
        :type new_effect: Effect
        """
        if type(self) is not type(new_effect):
            return

        self.value += new_effect.value

        if new_effect.duration < self.duration:
            self.duration = new_effect.duration

        self.decay += new_effect.decay

        if new_effect.accuracy > self.accuracy:
            self.accuracy = new_effect.accuracy

        if not new_effect.removable:
            self.removable = False

        return

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

        if (target.is_alive()) and (self.duration == 0):
            target.hp = 0
        else:
            fail = "dead"

        return {
            "fail": fail,
        }
