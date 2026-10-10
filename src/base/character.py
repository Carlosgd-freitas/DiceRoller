"""Character module."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, List

from src.base.color import Color, ColorData
from src.base.monster import Monster
from src.registries.character import CharacterRegistry

if TYPE_CHECKING:
    from src.base.dice import Dice


class Character(Monster):
    """
    Character class.
    """

    global_id: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        CharacterRegistry.register(cls)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dice = self.get_starting_dice()

    @abstractmethod
    def get_starting_dice(self) -> List[Dice]:
        """
        Returns the starting Dice that will be used by the Class.

        :return: Starting dice of the Class.
        :rtype: List[Dice]
        """
        raise NotImplementedError

    def get_color(self) -> ColorData:
        """
        Returns the Class color data.
        """
        return {
            "background_color": None,
            "foreground_color": Color.WHITE,
            "intensity": "BRIGHT",
        }
