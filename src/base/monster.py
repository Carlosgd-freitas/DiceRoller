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

    :var control_type: If the Monster is controller by AI or the player. Default is AI.
    :vartype control_type: ControlType

    :var difficulty: Monster's difficulty level, which dictates how the AI will choose
    it's actions. Default is NORMAL.
    :vartype difficulty: Difficulty

    :var suffix: Monster's name suffix (e.g. Slime 'A').
    :vartype suffix: str
    """

    def __init__(
        self,
        skills: List[Skill] = None,
        control_type: ControlType = ControlType.AI,
        difficulty: Difficulty = Difficulty.NORMAL,
        suffix: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.skills = [] if skills is None else skills
        self.control_type = control_type
        self.difficulty = difficulty
        self.suffix = suffix
