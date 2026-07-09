"""Randomizer module."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from random import choice, random, randrange, uniform
from typing import TYPE_CHECKING, List, Literal, Tuple
from uuid import uuid4

from src.base.dice import Dice
from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.base.team import Team
from src.combat.manager import CombatData
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.systems.settings import Settings

CHANCE_CALCULATION_METHOD = Literal[
    "LINEAR_DECAY", "QUADRATIC_DECAY", "EXPONENTIAL_INTERPOLATION"
]


@dataclass
class RandomizerConfig:
    """
    RandomizerConfig dataclass.

    :param team_threshold: Generated Combats will have a number of teams in this
    closed interval. Default value is [1, 5].
    :type team_threshold: Tuple[int, int]

    :param member_threshold: Generated Teams will have a number of monsters in this
    closed interval. Default value is [1, 5].
    :type member_threshold: Tuple[int, int]

    :param hp_threshold: Generated Monsters will have hp in this closed interval.
    Default value is [1, 100].
    :type hp_threshold: Tuple[int, int]

    :param mana_threshold: Generated Monsters will have mana in this closed interval.
    Default value is [0, 0].
    :type mana_threshold: Tuple[int, int]

    :param speed_threshold: Generated Monsters will have speed in this closed interval.
    Default value is [1, 100].
    :type speed_threshold: Tuple[int, int]

    :param dice_threshold: Generated Monsters will have a number of dice in this closed
    interval. Default value is [1, 4].
    :type dice_threshold: Tuple[int, int]

    :param side_threshold: Generated Dice will have a number of sides in this closed
    interval. Default value is [4, 8].
    :type side_threshold: Tuple[int, int]

    :param effect_threshold: Generated Sides will have a number of effects in this closed
    interval. Default value is [1, 3].
    :type effect_threshold: Tuple[int, int]

    :param target_keywords_threshold: Generated Effects will have a number of target
    keywords in this closed interval. Default value is [1, 3].
    :type target_keywords_threshold: Tuple[int, int]

    :param value_threshold: Generated Effects will have a value in this closed interval.
    Default value is [1, 100].
    :type value_threshold: Tuple[float, float]

    :param value_percent_threshold: Generated Effects will have a value (%) in this
    closed interval. Default value is [0.01, 0.25] (1%, 25%).
    :type value_percent_threshold: Tuple[float, float]

    :param duration_threshold: Generated Effects will have a duration in this closed
    interval. Default value is [2, 10].
    :type duration_threshold: Tuple[int, int]

    :param accuracy_threshold: Generated Effects will have an accuracy in this closed
    interval. Default value is [0.75, 1].
    :type accuracy_threshold: Tuple[float, float]

    :param effect_type: Generated Effects can only be of this type.
    :type effect_type: EffectType

    :param keyword_blacklist: Generated Effects can only have any keywords in this list.
    :type keyword_whitelist: List[Keyword]

    :param keyword_blacklist: Generated Effects won't have any keywords in this list.
    :type keyword_blacklist: List[Keyword]
    """

    # Combat attributes
    team_threshold: Tuple[int, int] = (1, 5)
    # Team attributes
    member_threshold: Tuple[int, int] = (1, 5)
    # Monster attributes
    hp_threshold: Tuple[int, int] = (1, 100)
    mana_threshold: Tuple[int, int] = (0, 0)
    speed_threshold: Tuple[int, int] = (1, 100)
    dice_threshold: Tuple[int, int] = (1, 4)
    # Dice attributes
    side_threshold: Tuple[int, int] = (4, 8)
    # Side attributes
    effect_threshold: Tuple[int, int] = (1, 3)
    target_keywords_threshold: Tuple[int, int] = (1, 3)
    # Effect attributes
    value_threshold: Tuple[float, float] = (1, 100)
    value_percent_threshold: Tuple[float, float] = (0.01, 0.25)
    duration_threshold: Tuple[int, int] = (1, 10)
    accuracy_threshold: Tuple[float, float] = (0.75, 1)
    effect_type: EffectType | None = None
    # Keyword attributes
    keyword_whitelist: list[Keyword] = field(default_factory=list)
    keyword_blacklist: list[Keyword] = field(default_factory=list)


class Randomizer:
    """
    Randomizer class.

    :var settings: Game settings.
    :vartype settings: Settings
    """

    def __init__(
        self,
        settings: Settings,
    ):
        self.logger = Logger(language=settings.language)

        self.all_effects = get_all_effects()
        self.all_monsters = get_all_monsters()

        self.monster_names = [
            "Alfa",
            "Bravo",
            "Charlie",
            "Delta",
            "Echo",
            "Foxtrot",
            "Golf",
            "Hotel",
            "India",
            "Juliett",
            "Kilo",
            "Lima",
            "Mike",
            "November",
            "Oscar",
            "Papa",
            "Quebec",
            "Romeo",
            "Sierra",
            "Tango",
            "Uniform",
            "Victor",
            "Whiskey",
            "X-ray",
            "Yankee",
            "Zulu",
        ]

        self.team_names = [
            "Alpha",
            "Beta",
            "Gamma",
            "Delta",
            "Epsilon",
            "Zeta",
            "Eta",
            "Theta",
            "Iota",
            "Kappa",
            "Lambda",
            "Mu",
            "Nu",
            "Xi",
            "Omicron",
            "Pi",
            "Rho",
            "Sigma",
            "Tau",
            "Upsilon",
            "Phi",
            "Chi",
            "Psi",
            "Omega",
        ]

    def _calculate_chance(
        self,
        index: int,
        threshold: Tuple[int, int],
        method: CHANCE_CALCULATION_METHOD = "QUADRATIC_DECAY",
    ) -> float:
        """
        Calculates the chance of continuing to generate a random object.

        The minimum threshold is always guaranteed. After reaching the minimum,
        the chance decreases until the maximum threshold is reached.

        :param index: Index of the current random generation attempt.
        :type index: int

        :param threshold: Threshold containing minimum and maximum values.
        :type threshold: Tuple[int, int]

        :param method: Chance calculation method.
        :type method: CHANCE_CALCULATION_METHOD

        :return: Calculated chance.
        :rtype: float
        """
        min_value, max_value = threshold

        # Guarantee minimum amount
        if index < min_value:
            return 1.0

        # Progress after minimum threshold.
        # Example:
        # threshold=(2, 5)
        # index=2 -> progress=0.25
        # index=4 -> progress=0.75
        progress = (index - min_value + 1) / (max_value - min_value + 1)
        progress = min(max(progress, 0.0), 1.0)

        if method == "LINEAR_DECAY":
            return 1.0 - progress

        if method == "QUADRATIC_DECAY":
            return (1.0 - progress) ** 2

        if method == "EXPONENTIAL_INTERPOLATION":
            return 0.5**progress

        raise ValueError(f"Unknown chance calculation method: {method}")

    def get_random_combat(
        self,
        config: RandomizerConfig | None = None,
    ) -> CombatData:
        """
        Gets a random combat. The maximum number of teams is 24.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Combat.
        :rtype: CombatData
        """
        # Setup
        config = config or RandomizerConfig()

        # Validation
        if config.team_threshold[1] > 24:
            raise ValueError("Maximum number of teams is 24.")

        # Randomizing
        teams: List[Team] = []
        team_names = deepcopy(self.team_names)

        for index in range(config.team_threshold[1]):
            chance = self._calculate_chance(index, config.team_threshold)

            if random() <= chance:
                team = self.get_random_team(config)

                if team.members:
                    # Guaranteeing an unique team name for each team
                    team.name = choice(team_names)
                    team_names.remove(team.name)

                    teams.append(team)
                else:
                    break

            else:
                break

        return {
            "teams": teams,
        }

    def get_random_team(
        self,
        config: RandomizerConfig | None = None,
    ) -> Team:
        """
        Gets a random Team with random monsters.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Team.
        :rtype: Team
        """
        # Setup
        config = config or RandomizerConfig()

        # Randomizing
        name = choice(self.team_names)

        members: List[Monster] = []

        for index in range(config.member_threshold[1]):
            chance = self._calculate_chance(index, config.member_threshold)

            if random() <= chance:
                member = self.get_random_monster(config)

                if member.dice:
                    members.append(member)
                else:
                    break

            else:
                break

        # Creating object
        team = Team(
            name=name,
            members=members,
        )

        return team

    def get_random_monster(
        self,
        config: RandomizerConfig | None = None,
    ) -> Monster:
        """
        Gets a random Monster with random Dice.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Monster.
        :rtype: Monster
        """
        # Setup
        config = config or RandomizerConfig()

        # Randomizing
        name = choice(self.monster_names)

        hp = randrange(config.hp_threshold[0], config.hp_threshold[1] + 1)
        mana = randrange(config.mana_threshold[0], config.mana_threshold[1] + 1)
        speed = randrange(config.speed_threshold[0], config.speed_threshold[1] + 1)

        dice: List[Dice] = []

        for index in range(config.dice_threshold[1]):
            chance = self._calculate_chance(index, config.dice_threshold)

            if random() <= chance:
                one_dice = self.get_random_dice(config)

                if one_dice.sides:
                    dice.append(one_dice)
                else:
                    break

            else:
                break

        # Creating object
        monster = Monster(
            global_id=uuid4(),
            name=name,
            hp=hp,
            max_hp=hp,
            speed=speed,
            mana=mana,
            dice=dice,
        )

        return monster

    def get_random_dice(
        self,
        config: RandomizerConfig | None = None,
    ) -> Dice:
        """
        Gets a random Dice with random Sides.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Side.
        :rtype: Side
        """
        # Setup
        config = config or RandomizerConfig()

        # Randomizing
        sides: List[Side] = []

        for index in range(config.side_threshold[1]):
            chance = self._calculate_chance(index, config.side_threshold)

            if random() <= chance:
                side = self.get_random_side(config)

                if side.effects:
                    sides.append(side)
                else:
                    break

            else:
                break

        # Creating object
        dice = Dice(sides)

        return dice

    def get_random_side(
        self,
        config: RandomizerConfig | None = None,
    ) -> Side:
        """
        Gets a random Side with effects of the same type.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Side.
        :rtype: Side
        """
        # Setup
        config = deepcopy(config or RandomizerConfig())

        if not config.effect_type:
            config.effect_type = choice(list(EffectType))

        # Randomizing
        effects: List[Effect] = []

        for index in range(config.effect_threshold[1]):
            chance = self._calculate_chance(index, config.effect_threshold)

            if random() <= chance:
                effect = self.get_random_effect(config)

                if effect:
                    effects.append(effect)
                    config.keyword_blacklist.append(effect.keyword)
                else:
                    break

            else:
                break

        weight = randrange(1, 6)

        # Creating object
        side = Side(effects, weight)

        return side

    def get_random_effect(
        self,
        config: RandomizerConfig | None = None,
    ) -> Effect:
        """
        Gets a random Effect.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Effect.
        :rtype: Effect
        """
        # Setup
        config = deepcopy(config or RandomizerConfig())

        # Filtering
        valid_effects = self.all_effects

        if config.effect_type:
            valid_effects = [
                effect for effect in valid_effects if effect.type == config.effect_type
            ]

        if config.keyword_whitelist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword in config.keyword_whitelist
            ]

        if config.keyword_blacklist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword not in config.keyword_blacklist
            ]

        # Randomizing
        if not valid_effects:
            return

        effect = deepcopy(choice(valid_effects))

        # Adjusting parameters
        effect.value = randrange(
            config.value_threshold[0], config.value_threshold[1] + 1
        )

        effect.value_percent = round(
            uniform(
                config.value_percent_threshold[0], config.value_percent_threshold[1]
            ),
            2,
        )

        effect.duration = randrange(
            config.duration_threshold[0], config.duration_threshold[1] + 1
        )

        effect.accuracy = round(
            uniform(config.accuracy_threshold[0], config.accuracy_threshold[1]), 2
        )

        # Adjusting target keywords
        target_keywords: List[Keyword] = []
        config.keyword_blacklist = [effect.keyword]

        for index in range(config.target_keywords_threshold[1]):
            chance = self._calculate_chance(index, config.target_keywords_threshold)

            if random() <= chance:
                keyword = self.get_random_keyword(config)

                if keyword:
                    target_keywords.append(keyword)
                    config.keyword_blacklist.append(keyword)
                else:
                    break

            else:
                break

        effect.target_keywords = target_keywords

        return effect

    def get_random_keyword(
        self,
        config: RandomizerConfig | None = None,
    ) -> Keyword:
        """
        Gets a random Keyword.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Keyword.
        :rtype: Keyword
        """
        # Setup
        config = config or RandomizerConfig()

        # Filtering
        valid_effects = self.all_effects

        if config.keyword_whitelist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword in config.keyword_whitelist
            ]

        if config.keyword_blacklist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword not in config.keyword_blacklist
            ]

        # Randomizing
        if not valid_effects:
            return

        effect = deepcopy(choice(valid_effects))

        return effect.keyword
