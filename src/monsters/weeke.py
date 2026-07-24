"""Weeke module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.block import BlockEffect
from src.effects.confuse import ConfuseEffect
from src.effects.corrupt import CorruptEffect
from src.effects.fragile import FragileEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.weak import WeakEffect


class Weeke(Monster):
    """
    Weeke class.
    """

    def __init__(self, **kwargs):
        dice_0 = Dice(
            sides=[
                Side([HealEffect(Stat(flat=1))]),
                Side([HealEffect(Stat(flat=2))]),
                Side([ManaEffect(Stat(flat=1))]),
                Side([ManaEffect(Stat(flat=2))]),
            ]
        )

        dice_1 = Dice(
            sides=[
                Side([WeakEffect(Stat(flat=1), duration=3)]),
                Side([FragileEffect(Stat(flat=1), duration=3)]),
                Side([ConfuseEffect(Stat(percent=0.5), duration=2)]),
                Side([CorruptEffect(Stat(flat=1))]),
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
            global_id="WEEKE",
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
