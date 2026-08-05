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
        duration: int = 2,
        accuracy: float = 1,
        removable: bool = True,
        target_keywords: List[Keyword] = None,
    ):
        target_keywords = [] if target_keywords is None else target_keywords

        super().__init__(
            keyword=Keyword.IMMUNITY,
            type=EffectType.BUFF,
            duration=duration,
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
