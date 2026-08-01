"""Randomizer module."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from math import inf
from random import choice, random, randrange, uniform
from typing import List, Literal, Tuple
from uuid import uuid4

from src.base.dice import Dice
from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.base.team import Team
from src.combat.manager import CombatData
from src.combat.order_strategy import OrderStrategy
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters

CHANCE_CALCULATION_METHOD = Literal[
    "LINEAR_DECAY", "QUADRATIC_DECAY", "EXPONENTIAL_INTERPOLATION"
]


@dataclass
class RandomizerConfig:
    """
    RandomizerConfig dataclass.

    :param team_threshold: Generated Combats will have a number of teams in this
    closed interval. Default value is [2, 4].
    :type team_threshold: Tuple[int, int]

    :param member_threshold: Generated Teams will have a number of monsters in this
    closed interval. Default value is [2, 5].
    :type member_threshold: Tuple[int, int]

    :param hp_threshold: Generated Monsters will have hp in this closed interval.
    Default value is [6, 60].
    :type hp_threshold: Tuple[int, int]

    :param mana_threshold: Generated Monsters will have mana in this closed interval.
    Default value is [0, 0].
    :type mana_threshold: Tuple[int, int]

    :param speed_threshold: Generated Monsters will have speed in this closed interval.
    Default value is [1, 10].
    :type speed_threshold: Tuple[int, int]

    :param dice_threshold: Generated Monsters will have a number of dice in this closed
    interval. Default value is [1, 3].
    :type dice_threshold: Tuple[int, int]

    :param side_threshold: Generated Dice will have a number of sides in this closed
    interval. Default value is [4, 8].
    :type side_threshold: Tuple[int, int]

    :param effect_threshold: Generated Sides will have a number of effects in this closed
    interval. Default value is [1, 3].
    :type effect_threshold: Tuple[int, int]

    :param value_flat_threshold: Generated Effects will have a flat value in this
    closed interval. Default value is [1, 8].
    :type value_threshold: Tuple[float, float]

    :param value_percent_threshold: Generated Effects will have a percent value in
    this closed interval. Default value is [0.01, 0.25] (1%, 25%).
    :type value_percent_threshold: Tuple[float, float]

    :param min_value_flat_threshold: Generated Effects will have a flat minimum value
    in this closed interval. Default value is [0, 0].
    :type min_value_threshold: Tuple[float, float]

    :param min_value_percent_threshold: Generated Effects will have a percent minimum
    value in this closed interval. Default value is [0, 0] (0%, 0%).
    :type min_value_percent_threshold: Tuple[float, float]

    :param max_value_flat_threshold: Generated Effects will have a flat maximum value
    in this closed interval. Default value is [inf, inf].
    :type max_value_threshold: Tuple[float, float]

    :param max_value_percent_threshold: Generated Effects will have a percent maximum
    value in this closed interval. Default value is [inf, inf] (inf%, inf%).
    :type max_value_percent_threshold: Tuple[float, float]

    :param duration_threshold: Generated Effects will have a duration in this closed
    interval. Default value is [2, 6].
    :type duration_threshold: Tuple[int, int]

    :param delta_flat_threshold: Generated Effects will have a flat delta in this
    closed interval. Default value is [0, 0].
    :type delta_threshold: Tuple[float, float]

    :param delta_percent_threshold: Generated Effects will have a percent delta in
    this closed interval. Default value is [0, 0] (0%, 0%).
    :type delta_percent_threshold: Tuple[float, float]

    :param accuracy_threshold: Generated Effects will have an accuracy (%) in this
    closed interval. Default value is [1, 1] (100%, 100%).
    :type accuracy_threshold: Tuple[float, float]

    :param target_keywords_threshold: Generated Effects will have a number of target
    keywords in this closed interval. Default value is [1, 3].
    :type target_keywords_threshold: Tuple[int, int]

    :param effect_type: Generated Effects can only be of this type.
    :type effect_type: EffectType

    :param flat_threshold: Generated Stats will have a flat value in this closed
    interval. Default value is [1, 20].
    :type threshold: Tuple[float, float]

    :param percent_threshold: Generated Stats will have a percent value in this closed
    interval. Default value is [0.01, 1] (1%, 100%).
    :type percent_threshold: Tuple[float, float]

    :param keyword_whitelist: Generated Effects can only have any keywords in this list.
    :type keyword_whitelist: List[Keyword]

    :param keyword_blacklist: Generated Effects won't have any keywords in this list.
    :type keyword_blacklist: List[Keyword]
    """

    # Combat attributes
    team_threshold: Tuple[int, int] = (2, 4)
    # Team attributes
    member_threshold: Tuple[int, int] = (2, 5)
    # Monster attributes
    hp_threshold: Tuple[int, int] = (6, 60)
    mana_threshold: Tuple[int, int] = (0, 0)
    speed_threshold: Tuple[int, int] = (1, 10)
    dice_threshold: Tuple[int, int] = (1, 3)
    # Dice attributes
    side_threshold: Tuple[int, int] = (4, 8)
    # Side attributes
    effect_threshold: Tuple[int, int] = (1, 3)
    # Effect attributes
    value_flat_threshold: Tuple[float, float] = (1, 8)
    value_percent_threshold: Tuple[float, float] = (0.01, 0.25)
    min_value_flat_threshold: Tuple[float, float] = (0, 0)
    min_value_percent_threshold: Tuple[float, float] = (0, 0)
    max_value_flat_threshold: Tuple[float, float] = (inf, inf)
    max_value_percent_threshold: Tuple[float, float] = (inf, inf)
    duration_threshold: Tuple[int, int] = (2, 6)
    delta_flat_threshold: Tuple[float, float] = (0, 0)
    delta_percent_threshold: Tuple[float, float] = (0, 0)
    accuracy_threshold: Tuple[float, float] = (1, 1)
    target_keywords_threshold: Tuple[int, int] = (1, 3)
    effect_type: EffectType | None = None
    # Stat attributes
    flat_threshold: Tuple[float, float] = (1, 20)
    percent_threshold: Tuple[float, float] = (0.01, 1)
    # Keyword attributes
    keyword_whitelist: list[Keyword] = field(default_factory=list)
    keyword_blacklist: list[Keyword] = field(default_factory=list)

    def __str__(self) -> str:
        """String representation of RandomizerConfig."""
        type = self.effect_type.value if self.effect_type else None
        keyword_whitelist = ", ".join(
            [str(keyword.name) for keyword in self.keyword_whitelist]
        )
        keyword_blacklist = ", ".join(
            [str(keyword.name) for keyword in self.keyword_blacklist]
        )

        _str = f"Team Threshold: {self.team_threshold}\n"
        _str += f"Member Threshold: {self.member_threshold}\n"
        _str += f"HP Threshold: {self.hp_threshold}\n"
        _str += f"Mana Threshold: {self.mana_threshold}\n"
        _str += f"Speed Threshold: {self.speed_threshold}\n"
        _str += f"Dice Threshold: {self.dice_threshold}\n"
        _str += f"Side Threshold: {self.side_threshold}\n"
        _str += f"Effect Threshold: {self.effect_threshold}\n"
        _str += f"Value Threshold: {self.value_flat_threshold}\n"
        _str += f"Value (%) Threshold: {self.value_percent_threshold}\n"
        _str += f"Min. Value Threshold: {self.min_value_flat_threshold}\n"
        _str += f"Min. Value (%) Threshold: {self.min_value_percent_threshold}\n"
        _str += f"Max. Value Threshold: {self.max_value_flat_threshold}\n"
        _str += f"Max. Value (%) Threshold: {self.max_value_percent_threshold}\n"
        _str += f"Duration Threshold: {self.duration_threshold}\n"
        _str += f"Delta Threshold: {self.delta_flat_threshold}\n"
        _str += f"Delta (%) Threshold: {self.delta_percent_threshold}\n"
        _str += f"Accuracy (%) Threshold: {self.accuracy_threshold}\n"
        _str += f"Target keywords Threshold: {self.target_keywords_threshold}\n"
        _str += f"Effect Type: {type}\n"
        _str += f"Flat Threshold: {self.flat_threshold}\n"
        _str += f"Percent Threshold: {self.percent_threshold}\n"
        _str += f"Keyword whitelist: {keyword_whitelist}\n"
        _str += f"Keyword blacklist: {keyword_blacklist}"

        return _str


class Randomizer:
    """
    Randomizer class.
    """

    def __init__(self):
        self.all_effects = get_all_effects()
        self.all_monsters = get_all_monsters()

        self.monster_names = [
            "Alpha",
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

    def random_int(
        self, threshold: Tuple[int, int], cap: Tuple[int, int] = None
    ) -> int:
        """
        Generates a random integer.

        :param threshold: Closed interval containing minimum and maximum for
        generating the integer.
        :type threshold: Tuple[int, int]

        :param cap: Numbers to substitute -inf and inf values. Default value is
        [-999, 999].
        :type cap: int

        :return: Random integer.
        :rtype: int
        """
        cap = [-999, 999] if cap is None else cap
        min_value, max_value = threshold

        if min_value == -inf:
            min_value = cap[0]
        elif min_value == inf:
            min_value = cap[1]

        if max_value == -inf:
            max_value = cap[0]
        elif max_value == inf:
            max_value = cap[1]

        value = randrange(min_value, max_value + 1)

        return value

    def random_float(self, threshold: Tuple[float, float]) -> float:
        """
        Generates a random float.

        :param threshold: A closed interval containing minimum and maximum for
        generating the float.
        :type threshold: Tuple[float, float]

        :return: Random float.
        :rtype: float
        """
        min_value, max_value = threshold

        if min_value == -inf or max_value == -inf:
            return -inf
        elif min_value == inf or max_value == inf:
            return inf
        else:
            return round(
                uniform(min_value, max_value),
                2,
            )

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
        order_strategy = choice(list(OrderStrategy))

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
            "order_strategy": order_strategy,
            "round": 1,
            "teams": teams,
            "turn": 1,
        }

    def get_random_team_name(self) -> str:
        """
        Gets a random Team name.

        :return: Random Team name.
        :rtype: str
        """
        return choice(self.team_names)

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
        name = self.get_random_team_name()

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

    def get_random_monster_name(self) -> str:
        """
        Gets a random Monster name.

        :return: Random Monster name.
        :rtype: str
        """
        return choice(self.monster_names)

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
        name = self.get_random_monster_name()
        hp = self.random_int(config.hp_threshold)
        mana = self.random_int(config.mana_threshold)
        speed = self.random_int(config.speed_threshold)

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

        # Randomizing
        effects: List[Effect] = []

        for index in range(config.effect_threshold[1]):
            chance = self._calculate_chance(index, config.effect_threshold)

            if random() <= chance:
                effect = self.get_random_effect(config)

                if effect:
                    effects.append(effect)
                    config.keyword_blacklist.append(effect.keyword)

                    if config.effect_type is None:
                        config.effect_type = effect.type

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
        if effect.value is not None:
            if effect.value.flat is not None:
                effect.value.flat = self.random_int(config.value_flat_threshold)
            if effect.value.percent is not None:
                effect.value.percent = self.random_float(config.value_percent_threshold)

        if effect.min_value is not None:
            if effect.min_value.flat is not None:
                effect.min_value.flat = self.random_int(config.min_value_flat_threshold)
            if effect.min_value.percent is not None:
                effect.min_value.percent = self.random_float(
                    config.min_value_percent_threshold
                )

        if effect.max_value is not None:
            if effect.max_value.flat is not None:
                effect.max_value.flat = self.random_int(config.max_value_flat_threshold)
            if effect.max_value.percent is not None:
                effect.max_value.percent = self.random_float(
                    config.max_value_percent_threshold
                )

        if effect.duration is not None:
            effect.duration = self.random_int(config.duration_threshold)

        if effect.delta is not None:
            if effect.delta.flat is not None:
                effect.delta.flat = self.random_int(config.delta_flat_threshold)
            if effect.delta.percent is not None:
                effect.delta.percent = self.random_float(config.delta_percent_threshold)

        if effect.accuracy is not None:
            effect.accuracy = self.random_float(config.accuracy_threshold)

        if effect.target_keywords is not None:
            target_keywords: List[Keyword] = []

            config.keyword_whitelist = []
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

    def get_random_stat(
        self,
        config: RandomizerConfig | None = None,
    ) -> Stat:
        """
        Gets a random Stat.

        :param config: Randomizer Configuration.
        :type config: RandomizerConfig

        :return: Random Stat.
        :rtype: Stat
        """
        # Setup
        config = config or RandomizerConfig()

        # Randomizing
        flat = self.random_int(config.flat_threshold)
        percent = self.random_float(config.percent_threshold)

        # Creating object
        side = Stat(flat, percent)

        return side
