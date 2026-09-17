"""Delay effect module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class DelayEffect(Effect):
    """
    Delay Effect.

    Extends the duration of effects on target.
    """

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        accuracy: float = 1,
        target_keywords: List[Keyword] = None,
    ):
        if value is None:
            value = Stat(flat=0, percent=0)
        if min_value is None:
            min_value = Stat(flat=0, percent=0)
        if max_value is None:
            max_value = Stat(flat=inf, percent=inf)

        target_keywords = [] if target_keywords is None else target_keywords

        super().__init__(
            keyword=Keyword.DELAY,
            type=EffectType.UTILITY,
            value=value,
            min_value=min_value,
            max_value=max_value,
            accuracy=accuracy,
            persistent=False,
            target_keywords=target_keywords,
        )

    def get_valid_target_keywords(self) -> List[Keyword]:
        """
        Returns a list containing the valid targt keywords for the Effect.

        :return: Valid targt keywords for the Effect.
        :rtype: List[Keyword]
        """
        return [
            Keyword.ALL,
            Keyword.ABSORB,
            Keyword.BLIND,
            Keyword.BLOCK,
            Keyword.BLEED,
            Keyword.BURN,
            Keyword.CONFUSE,
            Keyword.DOOM,
            Keyword.FOCUS,
            Keyword.FORTIFY,
            Keyword.FRAGILE,
            Keyword.FREEZE,
            Keyword.FROSTBURN,
            Keyword.HASTE,
            Keyword.IMMUNITY,
            Keyword.INVISIBLE,
            Keyword.INVULNERABLE,
            Keyword.MANA_REGEN,
            Keyword.OIL,
            Keyword.POISON,
            Keyword.REGEN,
            Keyword.REPEL,
            Keyword.SACRED_BLOCK,
            Keyword.SLEEP,
            Keyword.SLOW,
            Keyword.STRENGTH,
            Keyword.STUN,
            Keyword.TAUNT,
            Keyword.THORNS,
            Keyword.WEAK,
        ]

    def get_description_variable_key(self) -> str:
        """
        Returns a message key for the Effect description that takes the parameters into
        consideration.

        :return: The message key.
        :rtype: str
        """
        if Keyword.ALL in self.target_keywords:
            key = "description_all_"
        elif self.target_keywords:
            key = "description_specific_"
        else:
            return "description"

        if (not self.value.flat) and (not self.value.percent):
            key += "flat"
        elif (self.value.flat) and (not self.value.percent):
            key += "flat"
        elif (not self.value.flat) and (self.value.percent):
            key += "percent"
        else:
            key += "both"

        return key

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
        for effect in target.effects:
            if (
                (self.value is not None)
                and (self.target_keywords)
                and (
                    effect.keyword in self.target_keywords
                    or Keyword.ALL in self.target_keywords
                )
                and (effect.duration is not None)
            ):
                effective_value = 0

                if self.value.flat is not None:
                    effective_value += self.value.flat
                if self.value.percent is not None:
                    effective_value += self.value.percent * effect.duration

                effect.duration += effective_value

        return {}
