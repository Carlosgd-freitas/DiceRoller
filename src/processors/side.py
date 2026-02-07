"""Side processor module."""

from typing import List
from base.side import Side
from base.monster import Monster
from base.keywords import Keyword


def process_side(
    side: Side,
    targets: List[Monster]
) -> List[Monster]:
    raise NotImplementedError()
