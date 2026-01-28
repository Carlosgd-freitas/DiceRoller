"""Monster module."""

from enum import Enum
from typing import List
from base.skill import Skill
from base.entity import Entity


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
    """

    def __init__(
        self,
        skills: List[Skill] = [],
        control_type: ControlType = ControlType.AI,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.skills: List[Skill] = skills
        self.control_type = control_type
