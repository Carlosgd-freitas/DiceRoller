"""Mana Spirit module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
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
                Side([ManaEffect(1)]),
                Side([ManaEffect(1)]),
                Side([ManaEffect(2)]),
                Side([ManaEffect(2)]),
                Side([ManaEffect(3)]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([HealEffect(1)]),
                Side([HealEffect(2)]),
                Side([HealEffect(2)]),
                Side([HealEffect(3)]),
                Side([HealEffect(2), CleanseEffect(1)]),
            ]
        )

        dice_2 = Dice(
            sides=[
                Side([BlockEffect(1)]),
                Side([BlockEffect(1)]),
                Side([BlockEffect(2)]),
                Side([BlockEffect(2)]),
                Side([BlockEffect(3)]),
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
