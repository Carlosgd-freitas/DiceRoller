"""Pain effect module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.processors.damage import calculate_damage

if TYPE_CHECKING:
    from src.base.entity import Entity


class PainEffect(Effect):
    """
    Pain Effect.

    Will reduce self's HP by the effect value.
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
            keyword=Keyword.PAIN,
            value=value,
            value_percent=value_percent,
            duration=duration,
            decay=decay,
            accuracy=accuracy,
            type=EffectType.CURSE,
            persistent=False,
            removable=removable,
            target_keywords=target_keywords,
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
            "attribute": "hp",
            "fail": fail,
        }
