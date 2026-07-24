"""Mana Spirit module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.block import BlockEffect
from src.effects.cleanse import CleanseEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect


class ManaSpirit(Monster):
    """
    Mana Spirit class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([ManaEffect(Stat(flat=1))]),
                Side([ManaEffect(Stat(flat=1))]),
                Side([ManaEffect(Stat(flat=2))]),
                Side([ManaEffect(Stat(flat=2))]),
                Side([ManaEffect(Stat(flat=3))]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([HealEffect(Stat(flat=1))]),
                Side([HealEffect(Stat(flat=2))]),
                Side([HealEffect(Stat(flat=2))]),
                Side([HealEffect(Stat(flat=3))]),
                Side([HealEffect(Stat(flat=2)), CleanseEffect(Stat(flat=1))]),
            ]
        )

        dice_2 = Dice(
            sides=[
                Side([BlockEffect(Stat(flat=1))]),
                Side([BlockEffect(Stat(flat=1))]),
                Side([BlockEffect(Stat(flat=2))]),
                Side([BlockEffect(Stat(flat=2))]),
                Side([BlockEffect(Stat(flat=3))]),
            ]
        )

        super().__init__(
            global_id="MANA_SPIRIT",
            dice=[
                dice_0,
                dice_1,
                dice_2,
            ],
            hp=6,
            max_hp=6,
            speed=1,
            mana=0,
            **kwargs
        )
