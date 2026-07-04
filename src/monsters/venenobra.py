"""Venenobra module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.poison import PoisonEffect


class Venenobra(Monster):
    """
    Venenobra class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([PoisonEffect(1, duration=3)]),
                Side([PoisonEffect(2, duration=3)]),
                Side([AttackEffect(1), PoisonEffect(1, duration=3)]),
                Side([AttackEffect(1), PoisonEffect(2, duration=3)]),
                Side([AttackEffect(2), PoisonEffect(1, duration=3)]),
                Side([AttackEffect(2), PoisonEffect(2, duration=3)]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([BlockEffect(1)]),
                Side([BlockEffect(1)]),
                Side([BlockEffect(2)]),
                Side([BlockEffect(2)]),
            ]
        )

        super().__init__(
            global_id="VENENOBRA",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=6,
            max_hp=6,
            speed=2,
            mana=0,
            **kwargs
        )
