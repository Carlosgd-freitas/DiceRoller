"""Skill module."""

from enum import Enum
from base.entity import Entity


class SkillType(Enum):
    """Type of a Skill."""

    ACTIVE = "ACTIVE"
    PASSIVE = "PASSIVE"


class Skill(Entity):
    """
    Skill class.

    :var type: Skill's type.
    :vartype type: SkillType
    """

    def __init__(
        self,
        type: SkillType = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.type: SkillType = type
