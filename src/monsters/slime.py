from src.base.side import Side
from src.base.dice import Dice
from src.base.monster import Monster
from src.effects.block import BlockEffect
from src.effects.attack import AttackEffect

class Slime(Monster):
    """
    Slime class.
    """

    def __init__(
        self,
        **kwargs
    ):
        attacking_sides = []
        blocking_sides = []

        for i in range(1, 5):
            attacking_sides.append(Side([AttackEffect(i)]))
            blocking_sides.append(Side([BlockEffect(i)]))

        dice_0 = Dice(sides=attacking_sides)
        dice_1 = Dice(sides=blocking_sides)

        super().__init__(
            global_id="MONSTER_0",
            dice=[
                dice_0,
                dice_1,
            ],
            hp=6,
            max_hp=6,
            speed=1,
            mana=0,
            **kwargs
        )
