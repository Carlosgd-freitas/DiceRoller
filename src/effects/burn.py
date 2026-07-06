"""Burn effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.triggers import Trigger
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class BurnEffect(Effect):
    """
    Burn Effect.

    This is a debuff which will reduce the target's HP by the effect value at the start
    of each of the target's turn. Removes Freeze when applied.
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
            keyword=Keyword.BURN,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.DEBUFF,
            trigger=Trigger.TURN_START,
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

        if target:
            oil = target.get_effect(Keyword.OIL)
            if oil:
                effective_value += oil.value

        return effective_value

    def on_apply(
        self,
        source: Entity,
        target: Entity,
    ) -> EffectData:
        fail = None
        removed_effects = []

        if target.is_alive():
            freeze = target.remove_effect(Keyword.FREEZE)
            if freeze:
                removed_effects.append(freeze)

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
        damage_data = {}
        fail = None

        if target.is_alive():
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
        }
