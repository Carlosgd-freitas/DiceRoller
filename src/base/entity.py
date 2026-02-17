"""Entity module."""

from uuid import uuid4
from typing import List
from src.base.dice import Dice
from src.base.side import Side
from src.base.effect import Effect
from src.base.keywords import Keyword


class Entity():
    """
    Entity class.
    
    :var global_id: All objects of the same Entity subclass will have this same
    identifier.
    :vartype id: str

    :var local_id: Each Entity object will have its own identifier. The default value
    is a generated UUID version 4 in str format.
    :vartype id: str

    :var name: Entity's name.
    :vartype name: str

    :var description: Entity's description.
    :vartype description: str

    :var hp: Entity's current health points.
    :vartype hp: int

    :var max_hp: Entity's maximum health points.
    :vartype max_hp: int

    :var speed: Entity's speed.
    :vartype speed: int

    :var dice: Entity's dice.
    :vartype dice: List[Dice]

    :var effects: Entity's effects.
    :vartype effects: List[Effect]
    """

    def __init__(
        self,
        global_id: str = None,
        local_id: str = str(uuid4()),
        name: str = None,
        description: str = None,
        hp: int = None,
        max_hp: int = None,
        speed: int = None,
        dice: List[Dice] = None,
        effects: List[Effect] = None,
        **kwargs
    ):
        self.global_id: str = global_id
        self.local_id: str = local_id

        self.name: str = name
        self.description: str = description

        self.hp: int = hp
        self.max_hp: int = max_hp
        self.speed: int = speed

        self.dice: List[Dice] = dice
        self.effects: List[Effect] = effects

        self.dice = [] if dice is None else list(dice)
        self.effects = [] if effects is None else list(effects)

    def roll(self) -> List[Side]:
        """
        Randomly returns list of sides; one for each of this Entity's dice.

        :return: A list of Side objects.
        :rtype: List[Side]
        """

        rolled = [
            dice.roll()
            for dice in self.dice
        ]

        return rolled

    def equalize_stats(self) -> None:
        """
        Equalize stats to acceptable values:
        * Entity's HP will be changed to [0, max_hp] interval.
        """
        if self.hp < 0:
            self.hp = 0
        elif self.hp > self.max_hp:
            self.hp = self.max_hp
        return

    def get_effect(self, keyword: Keyword) -> Effect:
        """
        Returns a effect from the entity based on a keyword.

        :param keyword: A keyword.
        :type keyword: Keyword

        :return: An effect.
        :rtype: Effect
        """
        for effect in self.effects:
            if effect.keyword == keyword:
                return effect
        return None
