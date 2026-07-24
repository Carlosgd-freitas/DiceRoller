"""Slime module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect


class Slime(Monster):
    """
    Slime class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(Stat(flat=1))]),
                Side([AttackEffect(Stat(flat=2))]),
                Side([AttackEffect(Stat(flat=3))]),
                Side([AttackEffect(Stat(flat=4))]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([BlockEffect(Stat(flat=1))]),
                Side([BlockEffect(Stat(flat=2))]),
                Side([BlockEffect(Stat(flat=3))]),
                Side([BlockEffect(Stat(flat=4))]),
            ]
        )

        super().__init__(
            global_id="SLIME",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=6,
            max_hp=6,
            speed=1,
            mana=0,
            **kwargs
        )
