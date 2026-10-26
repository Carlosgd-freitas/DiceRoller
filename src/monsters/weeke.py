"""Weeke module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.entity import AttributeData
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.block import BlockEffect
from src.effects.confuse import ConfuseEffect
from src.effects.corrupt import CorruptEffect
from src.effects.fragile import FragileEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.weak import WeakEffect


class Weeke(Monster):
    """
    Weeke class.
    """

    global_id = "WEEKE"

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

        if difficulty.value < 4:
            speed = 1
        else:
            speed = 2

        return {
            "hp": 6,
            "max_hp": 6,
            "speed": speed,
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
                    Side([HealEffect(Stat(flat=1, percent=0))]),
                    Side([ManaEffect(Stat(flat=1, percent=0))]),
                    Side(
                        [
                            HealEffect(Stat(flat=1, percent=0)),
                            ManaEffect(Stat(flat=1, percent=0)),
                        ]
                    ),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([WeakEffect(Stat(flat=1, percent=0), duration=3)]),
                    Side([FragileEffect(Stat(flat=1, percent=0), duration=3)]),
                    Side([ConfuseEffect(Stat(percent=0.5), duration=3)]),
                    Side([CorruptEffect(Stat(flat=1))]),
                ]
            )

            dice = [dice_0, dice_1]

        else:
            dice_0 = Dice(
                sides=[
                    Side([HealEffect(Stat(flat=2, percent=0))]),
                    Side([ManaEffect(Stat(flat=2, percent=0))]),
                    Side(
                        [
                            HealEffect(Stat(flat=2, percent=0)),
                            ManaEffect(Stat(flat=2, percent=0)),
                        ]
                    ),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([WeakEffect(Stat(flat=1, percent=0), duration=6)]),
                    Side([FragileEffect(Stat(flat=1, percent=0), duration=6)]),
                    Side([ConfuseEffect(Stat(percent=0.75), duration=2)]),
                    Side([CorruptEffect(Stat(flat=2))]),
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
