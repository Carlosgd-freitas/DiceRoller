"""Training Dummy module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
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

    def get_dice(self, difficulty: Difficulty) -> List[Dice]:
        """
        Returns the Dice that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Dice that will be used by the Monster.
        :rtype: List[Dice]
        """
        dice_0 = Dice(
            sides=[
                Side([NothingEffect()]),
            ]
        )

        dice = [dice_0]

        return dice
