"""Tortuga module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.pierce import PierceEffect


class Tortuga(Monster):
    """
    Tortuga class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(1)]),
                Side([AttackEffect(1)]),
                Side([AttackEffect(2)]),
                Side([AttackEffect(2)]),
                Side([AttackEffect(2)]),
                Side([PierceEffect(4)]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([BlockEffect(1)]),
                Side([BlockEffect(2)]),
                Side([BlockEffect(3)]),
                Side([BlockEffect(4)]),
                Side([BlockEffect(5)]),
                Side([BlockEffect(6)]),
                Side([BlockEffect(7)]),
                Side([BlockEffect(8)]),
            ]
        )

        super().__init__(
            global_id="TORTUGA",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=10,
            max_hp=10,
            speed=1,
            mana=0,
            **kwargs
        )
