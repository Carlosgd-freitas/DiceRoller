"""Effect module."""

from src.base.keywords import Keyword, color_keyword


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

    :var chance: Effect's chance of being applied, in interval [0, 1]. Default value is
    1 (100%).
    :vartype chance: float

    :var dispellable: If the effect can be removed or not. Default is True.
    :vartype dispellable: bool
    """

    def __init__(
        self,
        keyword: Keyword,
        value: float = None,
        duration: int = None,
        decay: float = None,
        chance: float = 1.0,
        dispellable: bool = True,
    ):
        self.keyword = keyword
        self.value = value
        self.duration = duration
        self.decay = decay
        self.chance = chance
        self.dispellable = dispellable

    def __str__(self) -> str:
        _str = f"{color_keyword(self.keyword)}"

        if self.value:
            _str += f" {self.value}"
        if self.duration:
            _str += f" [{self.duration} Turns]"

        return _str
