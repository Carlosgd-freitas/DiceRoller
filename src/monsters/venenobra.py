"""Venenobra module."""

from typing import List

from src.base.dice import Dice
from src.base.difficulties import Difficulty
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
        super().__init__(
            global_id="VENENOBRA", hp=6, max_hp=6, speed=2, mana=0, **kwargs
        )

    def get_dice(self, difficulty: Difficulty) -> List[Dice]:
        """
        Returns the Dice that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Dice that will be used by the Monster.
        :rtype: List[Dice]
        """
        dice: List[Dice] = []

        if difficulty.value < 3:
            dice_0 = Dice(
                sides=[
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([PoisonEffect(Stat(flat=1, percent=0), duration=3)]),
                    Side(
                        [
                            AttackEffect(Stat(flat=1, percent=0)),
                            PoisonEffect(Stat(flat=1, percent=0), duration=3),
                        ]
                    ),
                    Side(
                        [
                            AttackEffect(Stat(flat=2, percent=0)),
                            PoisonEffect(Stat(flat=1, percent=0), duration=3),
                        ]
                    ),
                ]
            )

            dice_1 = Dice(
                sides=[
                    Side([BlockEffect(Stat(flat=1, percent=0))]),
                    Side([BlockEffect(Stat(flat=2, percent=0))]),
                ]
            )

        else:
            dice_0 = Dice(
                sides=[
                    Side([AttackEffect(Stat(flat=1, percent=0))]),
                    Side([PoisonEffect(Stat(flat=2, percent=0), duration=3)]),
                    Side(
                        [
                            AttackEffect(Stat(flat=1, percent=0)),
                            PoisonEffect(Stat(flat=2, percent=0), duration=3),
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
                    Side([BlockEffect(Stat(flat=2, percent=0))]),
                    Side([BlockEffect(Stat(flat=3, percent=0))]),
                ]
            )

        dice = [dice_0, dice_1]

        return dice
