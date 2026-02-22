from src.base.side import Side
from src.base.dice import Dice
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword


class Slime(Monster):
    """
    Slime class.
    """

    def __init__(
        self,
        **kwargs
    ):
        dice_0 = Dice(sides=[
            Side([Effect(Keyword.ATTACK, 1)]),
            Side([Effect(Keyword.ATTACK, 2)]),
            Side([Effect(Keyword.ATTACK, 3)]),
            Side([Effect(Keyword.ATTACK, 4)]),
        ])

        dice_1 = Dice(sides=[
            Side([Effect(Keyword.BLOCK, 1)]),
            Side([Effect(Keyword.BLOCK, 2)]),
            Side([Effect(Keyword.BLOCK, 3)]),
            Side([Effect(Keyword.BLOCK, 4)]),
        ])

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
