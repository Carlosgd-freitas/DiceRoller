"""Warrior module."""

from typing import List

from src.base.color import Color, ColorData
from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.entity import AttributeData
from src.base.side import Side
from src.base.stat import Stat
from src.classes.base_class import BaseClass
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect


class Warrior(BaseClass):
    """
    Warrior class.
    """

    global_id = "WARRIOR"

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
        return {
            "hp": 15,
            "max_hp": 15,
            "speed": 1,
            "mana": 0,
        }

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
                Side([AttackEffect(Stat(flat=5, percent=0))]),
                Side([AttackEffect(Stat(flat=6, percent=0))]),
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

        dice = [dice_0, dice_1]

        return dice

    def get_color(self) -> ColorData:
        """
        Returns the Class color data.
        """
        return {
            "background_color": None,
            "foreground_color": Color.RED,
            "intensity": "BRIGHT",
        }
