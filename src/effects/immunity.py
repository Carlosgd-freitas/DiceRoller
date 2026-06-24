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

    def __str__(self) -> str:
        """String representation of ImmunityEffect."""
        type = self.type.value if self.type else None
        trigger = self.trigger.value if self.trigger else None
        effects = ", ".join([str(effect) for effect in self.effects])

        _str = f"{self.keyword}"
        _str += f" | Value: {self.value}"
        _str += f" | Duration: {self.duration}"
        _str += f" | Decay: {self.decay}"
        _str += f" | Acc: {self.accuracy}"
        _str += f" | Type: {type}"
        _str += f" | Trigger: {trigger}"
        _str += f" | Persistent: {self.persistent}"
        _str += f" | Removable: {self.removable}"
        _str += f" | Effects: {effects}"

        return _str

    def stack(
        self,
        new_effect: ImmunityEffect,
    ):
        """
        Modifies the ImmunityEffect parameters based on a new effect, if both are of
        the same class:
        * value of both effects are summed.
        * the highest duration between the two effects is maintained.
        * decay of both effects are summed.
        * the highest accuracy between the two effects is maintained.
        * if the new effect is not removable, then the stacked effect will be also.
        * all effect immunities from the new effect will be added.

        :param new_effect: A new effect that is being applied to an Entity.
        :type new_effect: Effect
        """
        if type(self) is not type(new_effect):
            return

        self.value += new_effect.value

        if new_effect.duration > self.duration:
            self.duration = new_effect.duration

        self.decay += new_effect.decay

        if new_effect.accuracy > self.accuracy:
            self.accuracy = new_effect.accuracy

        if not new_effect.removable:
            self.removable = False

        for new_effect_immunity in new_effect.effects:
            if new_effect_immunity not in self.effects:
                self.effects.append(new_effect_immunity)

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
        if not target.is_alive():
            fail = "dead"

        return {
            "fail": fail,
        }
