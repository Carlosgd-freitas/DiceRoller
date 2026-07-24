"""Giant Slime module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect


class GiantSlime(Monster):
    """
    Giant Slime class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(Stat(flat=1))]),
                Side([AttackEffect(Stat(flat=2))]),
                Side([AttackEffect(Stat(flat=3))]),
                Side([AttackEffect(Stat(flat=4))]),
                Side([AttackEffect(Stat(flat=5))]),
                Side([AttackEffect(Stat(flat=6))]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([BlockEffect(Stat(flat=1))]),
                Side([BlockEffect(Stat(flat=2))]),
                Side([BlockEffect(Stat(flat=3))]),
                Side([BlockEffect(Stat(flat=4))]),
                Side([BlockEffect(Stat(flat=5))]),
                Side([BlockEffect(Stat(flat=6))]),
            ]
        )

        super().__init__(
            global_id="GIANT_SLIME",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=12,
            max_hp=12,
            speed=1,
            mana=0,
            **kwargs
        )
