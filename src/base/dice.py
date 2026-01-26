"""Dice class."""

from typing import List
from base.side import Side
from random import choices


class Dice:
    def __init__(self, sides = List[Side]):
        self.sides: List[Side] = sides

    def roll(self) -> Side:
        """
        Randomly returns one of the Dice's sides, based on each side weight.

        :return: A Side object.
        :rtype: Side
        """
        picked = choices(
            self.sides,
            weights=[side.weight for side in self.sides],
            k=1
        )[0]

        return picked
