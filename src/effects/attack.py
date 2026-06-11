"""Attack effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class AttackEffect(Effect):
    """
    Attack Effect.

    Will reduce the target's HP by the effect value and remove Sleep from it. The damage
    done will be affected by the target's Block.
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
            Keyword.ATTACK,
            value,
            duration,
            decay,
            accuracy,
            EffectType.OFFENSIVE,
            None,
            False,
            removable,
        )

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
                    Keyword.INVISIBLE,
                    Keyword.SACRED_BLOCK,
                ],
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
