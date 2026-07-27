"""Tortuga module."""

from src.base.dice import Dice
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
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(Stat(flat=1, percent=0))]),
                Side([AttackEffect(Stat(flat=1, percent=0))]),
                Side([AttackEffect(Stat(flat=2, percent=0))]),
                Side([AttackEffect(Stat(flat=2, percent=0))]),
                Side([AttackEffect(Stat(flat=2, percent=0))]),
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

        super().__init__(
            global_id="TORTUGA",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=10,
            max_hp=10,
            speed=0,
            mana=0,
            **kwargs
        )
