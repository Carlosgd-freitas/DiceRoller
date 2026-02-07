"""Monster module."""

from enum import Enum
from typing import List
from base.skill import Skill
from base.entity import Entity
from base.difficulties import Difficulty


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

    :var team: Monster's team name.
    :vartype team: str
    """

    def __init__(
        self,
        skills: List[Skill] = [],
        control_type: ControlType = ControlType.AI,
        difficulty: Difficulty = Difficulty.NORMAL,
        team: str = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.skills: List[Skill] = skills
        self.control_type = control_type
        self.difficulty = difficulty
        self.team = team
