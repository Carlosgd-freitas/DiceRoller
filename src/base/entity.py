"""Entity module."""

from typing import List
from base.dice import Dice
from base.side import Side


class Entity():
    """
    Entity class.
    
    :var id: Entity's unique identifier.
    :vartype id: str

    :var dice: Entity's dice.
    :vartype dice: List[Dice]

    :var name: Entity's name.
    :vartype name: str

    :var description: Entity's description.
    :vartype description: str

    :var hp: Entity's current health points.
    :vartype hp: int

    :var max_hp: Entity's maximum health points.
    :vartype max_hp: int
    """

    def __init__(
        self,
        id: str = None,
        dice: List[Dice] = [],
        name: str = None,
        description: str = None,
        hp: int = None,
        max_hp: int = None,
        **kwargs
    ):
        self.id: str = id
        self.dice: List[Dice] = dice

        self.name: str = name
        self.description: str = description

        self.hp: int = hp
        self.max_hp: int = max_hp

    def roll(self) -> List[Side]:
        """
        Randomly returns list of sides; one for each of this Entity's dice.

        :return: A list of Side objects.
        :rtype: List[Side]
        """

        picked = [
            dice.roll()
            for dice in self.dice
        ]

        return picked
