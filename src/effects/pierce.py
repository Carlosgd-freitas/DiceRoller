"""Pierce effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class PierceEffect(Effect):
    """
    Pierce Effect.

    Will reduce the target's HP by the effect value and remove Sleep from it. Ignores
    blocking-like effects.
    """

    def __init__(
        self,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        removable: bool = True,
    ):
        super().__init__(
            Keyword.PIERCE,
            value,
            duration,
            decay,
            accuracy,
            EffectType.OFFENSIVE,
            None,
            False,
            removable,
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
            strength = source.get_effect(Keyword.STRENGTH)
            if strength:
                effective_value += strength.value

            weak = source.get_effect(Keyword.WEAK)
            if weak:
                effective_value -= weak.value

        if effective_value < 0:
            effective_value = 0

        return effective_value

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
        damage_data = {}
        fail = None
        removed_effects = []

        if target.is_alive():
            sleep = target.remove_effect(Keyword.SLEEP)
            if sleep:
                removed_effects.append(sleep)

            damage_data = calculate_damage(
                self,
                source,
                target,
            )

            target.hp -= damage_data["damage"]
            target.equalize_stats()

        else:
            fail = "dead"

        return {
            **damage_data,
            "fail": fail,
            "removed_effects": removed_effects,
        }
