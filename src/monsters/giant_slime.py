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
