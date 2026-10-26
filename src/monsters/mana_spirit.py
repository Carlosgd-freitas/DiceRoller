"""Mana Spirit module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.entity import AttributeData
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.block import BlockEffect
from src.effects.cleanse import CleanseEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect


class ManaSpirit(Monster):
    """
    Mana Spirit class.
    """

    global_id = "MANA_SPIRIT"

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
            mana = 5

        return {
            "hp": 6,
            "max_hp": 6,
            "speed": 1,
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
            dice_0 = Dice(
                sides=[
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=3, percent=0))]),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([HealEffect(Stat(flat=1, percent=0))]),
                    Side([HealEffect(Stat(flat=2, percent=0))]),
                    Side([HealEffect(Stat(flat=2, percent=0))]),
                    Side([HealEffect(Stat(flat=2, percent=0))]),
                    Side([HealEffect(Stat(flat=3, percent=0))]),
                ]
            )

            dice = [dice_0, dice_1]

        else:
            dice_0 = Dice(
                sides=[
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=3, percent=0))]),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side(
                        [
                            HealEffect(Stat(flat=1, percent=0)),
                            CleanseEffect(Stat(flat=1)),
                        ]
                    ),
                    Side(
                        [
                            HealEffect(Stat(flat=2, percent=0)),
                            CleanseEffect(Stat(flat=1)),
                        ]
                    ),
                    Side(
                        [
                            HealEffect(Stat(flat=2, percent=0)),
                            CleanseEffect(Stat(flat=1)),
                        ]
                    ),
                    Side(
                        [
                            HealEffect(Stat(flat=2, percent=0)),
                            CleanseEffect(Stat(flat=1)),
                        ]
                    ),
                    Side(
                        [
                            HealEffect(Stat(flat=3, percent=0)),
                            CleanseEffect(Stat(flat=1)),
                        ]
                    ),
                ]
            )

            dice_2 = Dice(
                sides=[
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=2, percent=0))]),
                ]
            )

            dice = [dice_0, dice_1, dice_2]

        return dice
