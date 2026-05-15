"""Dice module."""

from __future__ import annotations

from random import choices
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.base.side import Side


class Dice:
    """
    Dice class.

    :var sides: Dice's sides.
    :vartype sides: List[Side]
    """

    def __init__(self, sides: List[Side] = None):
        self.sides = [] if sides is None else sides

    def roll(self) -> Side:
        """
        Randomly returns one of the Dice's sides, based on each side's weight.

        :return: A Side object.
        :rtype: Side
        """
        picked = choices(self.sides, weights=[side.weight for side in self.sides], k=1)[
            0
        ]

        return picked
