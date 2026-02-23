"""Effect module."""

from enum import Enum
from src.base.keywords import Keyword, color_keyword


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

    :var value: Effect's value.
    :vartype value: float

    :var duration: Effect's duration in turns, in relation to the Entity the Effect
    will be applied to.
    :vartype duration: int

    :var decay: Effect's value decay for each turn. A negative decay will increase the
    Effect's value instead.
    :vartype decay: float

    :var accuracy: Effect's chance of being applied, in interval [0, 1]. Default value is
    1 (100%).
    :vartype accuracy: float

    :var dispellable: If the effect can be removed or not. Default is True.
    :vartype dispellable: bool
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = 0,
        duration: int = 0,
        decay: float = 0,
        accuracy: float = 1,
        dispellable: bool = True,
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.accuracy = accuracy
        self.dispellable = dispellable

        if keyword in [
            Keyword.FORTIFY,
            Keyword.STRENGTHEN,
        ]:
            self.type = EffectType.BUFF

        elif keyword in [
            Keyword.BLEED,
            Keyword.BLIND,
            Keyword.BURN,
            Keyword.FRAGILE,
            Keyword.FREEZE,
            Keyword.POISON,
            Keyword.SLOW,
            Keyword.STUN,
            Keyword.WEAKEN,
        ]:
            self.type = EffectType.DEBUFF

        elif keyword in [
            Keyword.BLOCK,
            Keyword.DODGE,
        ]:
            self.type = EffectType.DEFENSIVE

        elif keyword in [
            Keyword.HEX
        ]:
            self.type = EffectType.DETERIORATION

        elif keyword in [
            Keyword.ATTACK,
            Keyword.CURSE,
            Keyword.PIERCE,
        ]:
            self.type = EffectType.OFFENSIVE

        elif keyword in [
            Keyword.CLEANSE,
            Keyword.HEAL,
            Keyword.MANA,
        ]:
            self.type = EffectType.RESTORATION

    def __str__(self) -> str:
        _str = f"{color_keyword(self.keyword)}"

        if self.value:
            _str += f" {self.value}"
        if self.duration:
            _str += f" [{self.duration} Turns]"

        return _str
