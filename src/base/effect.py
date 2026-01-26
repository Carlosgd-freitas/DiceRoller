"""Effect class."""

from src.base.keywords import Keyword


class Effect():
    def __init__(
        self,
        keyword: Keyword,
        value: float = None,
        duration: int = None,
        decay: int = None,
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

