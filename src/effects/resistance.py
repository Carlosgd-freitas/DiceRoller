"""Resistance effect module."""

from __future__ import annotations

from math import inf
from typing import TYPE_CHECKING, List

from src.base.effect import Effect, EffectData, EffectType
from src.base.keywords import Keyword
from src.base.stat import Stat

if TYPE_CHECKING:
    from src.base.entity import Entity


class ResistanceEffect(Effect):
    """
    Resistance Effect.

    Makes the target have a chance for effects to not be applied to it.
    """

    keyword = Keyword.RESISTANCE

    def __init__(
        self,
        value: Stat | None = None,
        min_value: Stat | None = None,
        max_value: Stat | None = None,
        duration: int = 2,
        delta: Stat | None = None,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        if value is None:
            value = Stat(percent=0)
        if min_value is None:
            min_value = Stat(percent=0)
        if max_value is None:
            max_value = Stat(percent=inf)
        if delta is None:
            delta = Stat(percent=0)

        target_keywords = [] if target_keywords is None else target_keywords

        super().__init__(
            keyword=self.keyword,
            type=EffectType.BUFF,
            value=value,
            min_value=min_value,
            max_value=max_value,
            duration=duration,
            delta=delta,
            accuracy=accuracy,
            persistent=True,
            removable=removable,
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
        if not self.target_keywords:
            return "description"
        elif Keyword.ALL in self.target_keywords:
            return "description_all"
        else:
            return "description_specific"

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
        return {}
