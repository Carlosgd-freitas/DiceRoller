"""Tortuga module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.pierce import PierceEffect


class Tortuga(Monster):
    """
    Tortuga class.
    """

    def __init__(self, **kwargs):
        super().__init__(
            global_id="TORTUGA", hp=10, max_hp=10, speed=0, mana=0, **kwargs
        )

    def get_dice(self, difficulty: Difficulty) -> List[Dice]:
        """
        Returns the Dice that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Dice that will be used by the Monster.
        :rtype: List[Dice]
        """
        dice: List[Dice] = []

        if difficulty.value < 3:
            dice_0 = Dice(
                sides=[
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=2, percent=0))]),
                    Side([AttackEffect(Stat(flat=2, percent=0))]),
                    Side([PierceEffect(Stat(flat=3, percent=0))]),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=2, percent=0))]),
                    Side([BlockEffect(Stat(flat=3, percent=0))]),
                    Side([BlockEffect(Stat(flat=4, percent=0))]),
                    Side([BlockEffect(Stat(flat=5, percent=0))]),
                    Side([BlockEffect(Stat(flat=6, percent=0))]),
                ]
            )

            dice = [dice_0]

        else:
            dice_0 = Dice(
                sides=[
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([AttackEffect(Stat(flat=2, percent=0))]),
                    Side([AttackEffect(Stat(flat=2, percent=0))]),
                    Side([AttackEffect(Stat(flat=4, percent=0))]),
                    Side([PierceEffect(Stat(flat=4, percent=0))]),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=2, percent=0))]),
                    Side([BlockEffect(Stat(flat=3, percent=0))]),
                    Side([BlockEffect(Stat(flat=4, percent=0))]),
                    Side([BlockEffect(Stat(flat=5, percent=0))]),
                    Side([BlockEffect(Stat(flat=6, percent=0))]),
                    Side([BlockEffect(Stat(flat=7, percent=0))]),
                    Side([BlockEffect(Stat(flat=8, percent=0))]),
                ]
            )

            dice = [dice_0, dice_1]

        return dice
