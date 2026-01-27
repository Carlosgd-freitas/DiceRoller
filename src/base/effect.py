"""Effect module."""

from src.base.keywords import Keyword


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

    :var chance: Effect's chance of being applied.
    :vartype chance: float
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = None,
        duration: int = None,
        decay: float = None,
        chance: float = None
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.chance = chance

    def __str__(self) -> str:
        _str = f"Keyword: {self.keyword.name}"

        if self.value:
            _str += f"; Value: {self.value}"
        if self.duration:
            _str += f"; Duration: {self.duration}"
        if self.decay:
            _str += f"; Decay: {self.decay}"
        if self.chance:
            _str += f"; Chance: {self.chance}"

        return _str

