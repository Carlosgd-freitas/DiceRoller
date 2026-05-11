"""Effect module."""

from enum import Enum
from typing import List
from src.base.triggers import Trigger
from src.base.keywords import (
    Keyword,
    color_keyword,
    get_incompatible_keywords,
)


class EffectType(Enum):
    """Type of Effect."""

    BUFF = "BUFF"
    DEBUFF = "DEBUFF"
    DEFENSIVE = "DEFENSIVE"
    DETERIORATION = "DETERIORATION"
    OFFENSIVE = "OFFENSIVE"
    RESTORATION = "RESTORATION"


class Effect():
    """
    Effect class.

    :var keyword: Effect's keyword.
    :vartype keyword: Keyword

    :var value: Effect's value. Default value is 0.
    :vartype value: float

    :var duration: Effect's duration in turns, in relation to the Entity the Effect
    will be applied to. Default value is 0.
    :vartype duration: int

    :var decay: Effect's value decay for each turn. A negative decay will increase the
    Effect's value instead. Default value is 0.
    :vartype decay: float

    :var accuracy: Effect's chance of being applied, in interval [0, 1]. Default value is
    1 (100%).
    :vartype accuracy: float

    :var type: Effect's type. By default, this value will depend on keyword.
    :vartype type: EffectType

    :var trigger: Effect's triggering condition. By default, this value will depend on
    keyword.
    :vartype trigger: Trigger

    :var incompatible: Effect's incompatible keywords, which will be removed if this Effect
    is added to an Entity. By default, this value will depend on keyword.
    :vartype incompatible: List[Keyword]
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        type: EffectType = None,
        trigger: Trigger = None,
        incompatible: List[Keyword] = None,
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.accuracy = accuracy

        self.type = type if type \
            else self._get_default_effect_type(self.keyword)

        self.trigger = trigger if trigger \
            else self._get_default_effect_trigger(self.keyword)

        self.incompatible = incompatible if incompatible \
            else get_incompatible_keywords(self.keyword)
        self.incompatible = self.incompatible if self.incompatible \
            else []

    def _get_default_effect_type(self, keyword: Keyword) -> EffectType:
        if keyword in [
            Keyword.FORTIFY,
            Keyword.STRENGTHEN,
        ]:
            return EffectType.BUFF

        elif keyword in [
            Keyword.BLEED,
            Keyword.BLIND,
            Keyword.BURN,
            Keyword.FRAGILE,
            Keyword.FREEZE,
            Keyword.POISON,
            Keyword.STUN,
            Keyword.WEAKEN,
        ]:
            return EffectType.DEBUFF

        elif keyword in [
            Keyword.BLOCK,
        ]:
            return EffectType.DEFENSIVE

        elif keyword in [
            Keyword.HEX,
        ]:
            return EffectType.DETERIORATION

        elif keyword in [
            Keyword.ATTACK,
            Keyword.CURSE,
            Keyword.DRAIN,
            Keyword.PIERCE,
        ]:
            return EffectType.OFFENSIVE

        elif keyword in [
            Keyword.HEAL,
            Keyword.MANA,
            Keyword.MANA_REGEN,
            Keyword.REGEN,
        ]:
            return EffectType.RESTORATION
        
        else:
            return None

    def _get_default_effect_trigger(self, keyword: Keyword) -> Trigger:
        if keyword in [
            Keyword.BLEED
        ]:
            return Trigger.ROLL

        if keyword in [
            Keyword.BURN,
            Keyword.MANA_REGEN,
            Keyword.POISON,
            Keyword.REGEN,
        ]:
            return Trigger.TURN_START

        else:
            return None

    def __str__(self) -> str:
        _str = f"{color_keyword(self.keyword)}"

        if self.value:
            _str += f" {self.value}"
        if self.duration:
            _str += f" [{self.duration} Turns]"

        return _str
