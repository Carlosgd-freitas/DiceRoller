"""Drain effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class DrainEffect(Effect):
    """
    Drain Effect.

    Will reduce the target's HP by the effect value, while increasing the source's HP
    and remove Sleep from it. The damage done will be affected by the target's Block.
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
            keyword=Keyword.DRAIN,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.OFFENSIVE,
            persistent=False,
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
                consider=[
                    Keyword.ABSORB,
                    Keyword.BLOCK,
                    Keyword.INVULNERABLE,
                    Keyword.SACRED_BLOCK,
                ],
            )

            target.hp -= damage_data["damage"]
            target.equalize_stats()

            source.hp += damage_data["damage"]
            source.equalize_stats()

        else:
            fail = "dead"

        return {
            **damage_data,
            "fail": fail,
            "removed_effects": removed_effects,
        }
