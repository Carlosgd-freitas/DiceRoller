"""Monster module."""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List

from src.base.difficulties import Difficulty
from src.base.entity import Entity

if TYPE_CHECKING:
    from src.base.skill import Skill


class ControlType(Enum):
    """Type of Monster control."""

    AI = "AI"
    PLAYER = "PLAYER"


class Monster(Entity):
    """
    Monster class.

    :var skills: Monster's skills.
    :vartype skills: List[Skill]

    :var control_type: If the Monster is controller by AI or the player. Default value
    is ControlType.AI.
    :vartype control_type: ControlType

    :var difficulty: Monster's difficulty level, which dictates how the AI will choose
    it's actions. Default is NORMAL.
    :vartype difficulty: Difficulty

    :var in_combat: If the monster is in combat. Default value is True.
    :vartype in_combat: bool

    :var turn_taken: If the monster has taken its turn. Default value is False.
    :vartype turn_taken: bool

    :var suffix: Monster's name suffix (e.g. Slime 'A').
    :vartype suffix: str
    """

    def __init__(
        self,
        skills: List[Skill] = None,
        control_type: ControlType = ControlType.AI,
        difficulty: Difficulty = Difficulty.NORMAL,
        in_combat: bool = True,
        turn_taken: bool = False,
        suffix: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.skills = [] if skills is None else skills
        self.control_type = control_type
        self.difficulty = difficulty
        self.in_combat = in_combat
        self.turn_taken = turn_taken
        self.suffix = suffix

    def __str__(self) -> str:
        """String representation of Monster."""
        _str = f"{self.name}"
        _str += f" | HP: {self.hp}/{self.max_hp}"
        _str += f" | Speed: {self.speed}"
        _str += f" | Mana: {self.mana}"

        _str += f"\n>>> Dice ({len(self.dice)}):"
        for one_dice in self.dice:
            _str += f"\n>> {one_dice}\n"

        return _str
