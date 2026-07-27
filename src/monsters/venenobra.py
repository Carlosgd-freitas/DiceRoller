"""Venenobra module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
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
                Side([PoisonEffect(Stat(flat=1, percent=0), duration=3)]),
                Side([PoisonEffect(Stat(flat=2, percent=0), duration=3)]),
                Side(
                    [
                        AttackEffect(Stat(flat=1, percent=0)),
                        PoisonEffect(Stat(flat=1, percent=0), duration=3),
                    ]
                ),
                Side(
                    [
                        AttackEffect(Stat(flat=1, percent=0)),
                        PoisonEffect(Stat(flat=2, percent=0), duration=3),
                    ]
                ),
                Side(
                    [
                        AttackEffect(Stat(flat=2, percent=0)),
                        PoisonEffect(Stat(flat=1, percent=0), duration=3),
                    ]
                ),
                Side(
                    [
                        AttackEffect(Stat(flat=2, percent=0)),
                        PoisonEffect(Stat(flat=2, percent=0), duration=3),
                    ]
                ),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([BlockEffect(Stat(flat=1, percent=0))]),
                Side([BlockEffect(Stat(flat=1, percent=0))]),
                Side([BlockEffect(Stat(flat=2, percent=0))]),
                Side([BlockEffect(Stat(flat=2, percent=0))]),
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
