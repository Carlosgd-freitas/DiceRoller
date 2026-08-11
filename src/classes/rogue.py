"""Rogue module."""

from copy import deepcopy
from typing import List

from src.base.dice import Dice
from src.base.side import Side
from src.base.stat import Stat
from src.classes.base_class import BaseClass
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.invisible import InvisibleEffect


class Rogue(BaseClass):
    """
    Rogue class.
    """

    def __init__(self, **kwargs):
        super().__init__(global_id="ROGUE", hp=12, max_hp=12, speed=1, mana=0, **kwargs)

    def get_starting_dice(self) -> List[Dice]:
        """
        Returns the starting Dice that will be used by the Class.

        :return: Starting dice of the Class.
        :rtype: List[Dice]
        """
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(Stat(flat=1, percent=0))]),
                Side([AttackEffect(Stat(flat=2, percent=0))]),
                Side([AttackEffect(Stat(flat=3, percent=0))]),
                Side([AttackEffect(Stat(flat=4, percent=0))]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([InvisibleEffect(duration=2)]),
                Side([BlockEffect(Stat(flat=1, percent=0))]),
                Side([BlockEffect(Stat(flat=1, percent=0))]),
                Side([BlockEffect(Stat(flat=2, percent=0))]),
                Side([BlockEffect(Stat(flat=2, percent=0))]),
                Side([BlockEffect(Stat(flat=3, percent=0))]),
            ]
        )

        dice = [dice_0, deepcopy(dice_0), dice_1]

        return dice
