"""Monster module."""

from typing import List
from base.skill import Skill
from base.entity import Entity


class Monster(Entity):
    """
    Monster class.

    :var skills: Monster's skills.
    :vartype skills: List[Skill]
    """

    def __init__(
        self,
        skills: List[Skill] = [],
        **kwargs
    ):
        super().__init__(**kwargs)
        self.skills: List[Skill] = skills
