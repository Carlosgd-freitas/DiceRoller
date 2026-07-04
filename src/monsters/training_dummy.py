"""Training Dummy module."""

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.effects.nothing import NothingEffect


class TrainingDummy(Monster):
    """
    Training Dummy class.
    """

    def __init__(self, **kwargs):
        dice = Dice(
            sides=[
                Side([NothingEffect()]),
            ]
        )

        super().__init__(
            global_id="TRAINING_DUMMY",
            dice=[dice],
            hp=6,
            max_hp=6,
            speed=0,
            mana=0,
            **kwargs
        )
