"""Training Dummy module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
from src.base.entity import AttributeData
from src.base.monster import Monster
from src.base.side import Side
from src.effects.nothing import NothingEffect


class TrainingDummy(Monster):
    """
    Training Dummy class.
    """

    global_id = "TRAINING_DUMMY"

    def __init__(self, **kwargs):
        super().__init__(global_id=self.global_id, **kwargs)

    def get_attributes(self, difficulty: Difficulty) -> AttributeData:
        """
        Returns the attributes of the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Attributes of the the Monster.
        :rtype: AttributeData
        """
        return {
            "hp": 6,
            "max_hp": 6,
            "speed": 0,
            "mana": 0,
        }

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
