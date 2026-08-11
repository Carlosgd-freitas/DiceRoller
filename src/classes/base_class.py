"""Base class module."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, List

from src.base.monster import Monster

if TYPE_CHECKING:
    from src.base.dice import Dice


class BaseClass(Monster):
    """
    BaseClass class.
    """

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
