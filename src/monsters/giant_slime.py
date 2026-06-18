"""Giant Slime module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect


class GiantSlime(Monster):
    """
    Giant Slime class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([AttackEffect(1)]),
                Side([AttackEffect(2)]),
                Side([AttackEffect(3)]),
                Side([AttackEffect(4)]),
                Side([AttackEffect(5)]),
                Side([AttackEffect(6)]),
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
            speed=2,
            mana=0,
            **kwargs
        )
