"""Monster module."""

from __future__ import annotations

from enum import Enum
from math import ceil
from typing import TYPE_CHECKING, List

from src.base.difficulties import Difficulty
from src.base.entity import AttributeData, Entity
from src.base.monster_registry import register_monster

if TYPE_CHECKING:
    from src.base.dice import Dice
    from src.base.skill import Skill


class ControlType(Enum):
    """Type of Monster control."""

    AI = "AI"
    PLAYER = "PLAYER"


class AILevel(Enum):
    """Monter IA level."""

    EASY = 0
    NORMAL = 1
    HARD = 2


class Monster(Entity):
    """
    Monster class.

    :var control_type: If the Monster is controller by AI or the player. Default value
    is ControlType.AI.
    :vartype control_type: ControlType

    :var difficulty: Game difficulty.
    :vartype difficulty: Difficulty

    :var ai_level: Monster AI level, which dictates AI behavior. Higher levels means
    smarter actions. Default is AILevel.NORMAL.
    :vartype ai_level: AILevel

    :var in_combat: If the monster is in combat. Default value is True.
    :vartype in_combat: bool

    :var turn_taken: If the monster has taken its turn. Default value is False.
    :vartype turn_taken: bool

    :var suffix: Monster's name suffix (e.g. Slime 'A').
    :vartype suffix: str
    """

    global_id: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_monster(cls)

    def __init__(
        self,
        control_type: ControlType = ControlType.AI,
        difficulty: Difficulty = Difficulty.NORMAL,
        in_combat: bool = True,
        turn_taken: bool = False,
        suffix: str = None,
        **kwargs,
    ):
        self.control_type = control_type
        self.in_combat = in_combat
        self.turn_taken = turn_taken
        self.suffix = suffix

        # Difficulty-based attributes
        attributes = self.get_attributes(difficulty)

        for attribute in ["hp", "max_hp", "speed", "mana"]:
            if attributes.get(attribute):
                kwargs[attribute] = attributes[attribute]

        for attribute in ["hp", "max_hp"]:
            attributes[attribute] = self.scale_hp(attributes[attribute], difficulty)

        super().__init__(**kwargs)

        self.ai_level = self.get_ai_level(difficulty)
        self.dice = self.get_dice(difficulty) or kwargs.get("dice", [])
        self.skills = self.get_skills(difficulty) or kwargs.get("skills", [])

    def __str__(self) -> str:
        """String representation of Monster."""
        _str = f"({self.global_id} | {self.local_id})"
        _str += f" {self.name} {self.suffix}"

        _str += f"\nHP: {self.hp}/{self.max_hp}"
        _str += f" | Speed: {self.speed}"
        _str += f" | Mana: {self.mana}"

        _str += f"\nControl Type: {self.control_type.name}"
        _str += f" | AI Level: {self.ai_level.name}"

        _str += f"\n>>> Dice ({len(self.dice)}):"
        for one_dice in self.dice:
            _str += f"\n>> {one_dice}\n"

        return _str

    def is_equivalent(self, monster: Monster) -> bool:
        """
        Compares two monsters and returns if they are equivalent.

        :param monster: Monster for comparison.
        :type monster: Monster

        :return: If the monsters are equivalent.
        :rtype: bool
        """
        return (
            isinstance(monster, Monster)
            and self.global_id == monster.global_id
            and self.hp == monster.hp
            and self.max_hp == monster.max_hp
            and len(self.dice) == len(monster.dice)
            and all(
                [
                    self_dice.is_equivalent(dice)
                    for self_dice, dice in zip(self.dice, monster.dice, strict=True)
                ]
            )
            and len(self.effects) == len(monster.effects)
            and all(
                [
                    self_effect.is_equivalent(effect)
                    for self_effect, effect in zip(
                        self.effects, monster.effects, strict=True
                    )
                ]
            )
        )

    def get_attributes(self, difficulty: Difficulty) -> AttributeData:
        """
        Returns the attributes of the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Attributes of the the Monster.
        :rtype: AttributeData
        """
        return {
            "hp": None,
            "max_hp": None,
            "speed": None,
            "mana": None,
        }

    def scale_hp(self, hp: int, difficulty: Difficulty) -> int:
        """
        Scales the Monster HP according to the game difficulty.

        :var hp: Initial Monster HP.
        :vartype hp: int

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Scaled Monster HP.
        :rtype: int
        """
        hp_scaling = 1

        if difficulty == Difficulty.EASY:
            hp_scaling = 0.5
        elif difficulty == Difficulty.HARD:
            hp_scaling = 1.25
        elif difficulty == Difficulty.EXPERT:
            hp_scaling = 1.5
        elif difficulty == Difficulty.MASTER:
            hp_scaling = 1.75
        elif difficulty == Difficulty.NIGHTMARE:
            hp_scaling = 2

        if hp is not None:
            return ceil(hp * hp_scaling)
        else:
            return 0

    def get_ai_level(self, difficulty: Difficulty) -> AILevel:
        """
        Returns the level of AI that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: AI Level that will be used by the Monster.
        :rtype: AILevel
        """
        if difficulty == Difficulty.EASY:
            return AILevel.EASY
        elif difficulty == Difficulty.NORMAL:
            return AILevel.NORMAL
        else:
            return AILevel.HARD

    def get_dice(self, difficulty: Difficulty) -> List[Dice]:
        """
        Returns the Dice that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Dice that will be used by the Monster.
        :rtype: List[Dice]
        """
        return []

    def get_skills(self, difficulty: Difficulty) -> List[Skill]:
        """
        Returns the skills that will be used by the Monster.

        :var difficulty: Game difficulty.
        :vartype difficulty: Difficulty

        :return: Skills that will be used by the Monster.
        :rtype: List[Skill]
        """
        return []
