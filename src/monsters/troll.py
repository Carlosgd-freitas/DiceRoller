"""Troll module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.entity import AttributeData
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.mana import ManaEffect


class Troll(Monster):
    """
    Troll class.
    """

    global_id = "TROLL"

    def __init__(self, **kwargs):
        super().__init__(global_id=self.global_id, **kwargs)

    def get_attributes(self, difficulty: Difficulty) -> AttributeData:
        """
        Returns the attributes of the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Attributes of the the Monster.
        :rtype: AttributeData
        """
        if difficulty.value < 3:
            mana = 0
        else:
            mana = 3

        return {
            "hp": 20,
            "max_hp": 20,
            "speed": 0,
            "mana": mana,
        }

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
            attacking_sides: List[Side] = []
            blocking_sides: List[Side] = []

            for i in range(1, 9):
                attacking_sides.append(Side([AttackEffect(Stat(flat=i, percent=0))]))
                blocking_sides.append(Side([BlockEffect(Stat(flat=i, percent=0))]))

            dice_0 = Dice(sides=attacking_sides)

            dice_1 = Dice(sides=blocking_sides)

            dice_2 = Dice(
                sides=[
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                ]
            )

            dice = [dice_0, dice_1, dice_2]

        else:
            attacking_sides: List[Side] = []
            blocking_sides: List[Side] = []

            for i in range(3, 11):
                attacking_sides.append(Side([AttackEffect(Stat(flat=i, percent=0))]))
                blocking_sides.append(Side([BlockEffect(Stat(flat=i, percent=0))]))

            dice_0 = Dice(sides=attacking_sides)

            dice_1 = Dice(sides=blocking_sides)

            dice_2 = Dice(
                sides=[
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                ]
            )

            dice = [dice_0, dice_1, dice_2]

        return dice
