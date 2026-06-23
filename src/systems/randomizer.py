"""Randomizer module."""

from __future__ import annotations

from copy import deepcopy
from random import choice, random, randrange, uniform
from typing import TYPE_CHECKING, List, Tuple
from uuid import uuid4

from src.base.dice import Dice
from src.base.effect import Effect, EffectType
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.combat.manager import CombatData
from src.combat.team import Team
from src.compendium.effects import get_all_effects
from src.compendium.monsters import get_all_monsters
from src.logger.logger import Logger

if TYPE_CHECKING:
    from src.effects.immunity import ImmunityEffect
    from src.systems.settings import Settings


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

    def get_random_combat(
        self,
        n_teams: int = 2,
        team_members: int = 3,
        hp_treshold: Tuple[int, int] = (1, 100),
        speed_treshold: Tuple[int, int] = (1, 100),
        max_dice: int = 4,
        max_sides: int = 8,
        max_effects: int = 3,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> CombatData:
        """
        Gets a random combat.

        :param n_teams: Number of teams. Maximum number is 24.
        :type n_teams: int

        :param team_members: Number of monsters in the team.
        :type team_members: int

        :param hp_treshold: The generated Monster will have hp in this closed interval.
        Default value is [1, 100].
        :type hp_treshold: Tuple[int, int]

        :param speed_treshold: The generated Monster will have speed in this closed interval.
        Default value is [1, 100].
        :type speed_treshold: Tuple[int, int]

        :param max_dice: Maximum number of dice. Default value is 4.
        :type max_dice: int

        :param max_sides: Maximum number of sides. Default value is 8.
        :type max_sides: int

        :param max_effects: Maximum number of effects on each side. Default value is 3.
        :type max_effects: int

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param effect_type: If effect_type is passed as a parameter, the returned Dice sides will
        have effects of that type. Otherwise, each side will have effects of a random type.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Side.
        :rtype: Side
        """
        # Validation
        if n_teams > 24:
            raise ValueError("n_teams maximum value is 24.")

        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        # Randomizing
        teams: List[Team] = []
        team_names = deepcopy(self.team_names)

        for _ in range(n_teams):
            team = self.get_random_team(
                team_members=team_members,
                hp_treshold=hp_treshold,
                speed_treshold=speed_treshold,
                max_dice=max_dice,
                max_sides=max_sides,
                max_effects=max_effects,
                value_treshold=value_treshold,
                duration_treshold=duration_treshold,
                accuracy_treshold=accuracy_treshold,
                effect_type=effect_type,
                keyword_whitelist=keyword_whitelist,
                keyword_blacklist=keyword_blacklist,
            )

            if team.members:
                # Guaranteeing an unique team name for each team
                team.name = choice(team_names)
                team_names.remove(team.name)

                teams.append(team)

        return {
            "teams": teams,
        }

    def get_random_team(
        self,
        team_members: int = 3,
        hp_treshold: Tuple[int, int] = (1, 100),
        speed_treshold: Tuple[int, int] = (1, 100),
        max_dice: int = 4,
        max_sides: int = 8,
        max_effects: int = 3,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Team:
        """
        Gets a random Team with random monsters.

        :param team_members: Number of monsters in the team.
        :type team_members: int

        :param hp_treshold: The generated Monster will have hp in this closed interval.
        Default value is [1, 100].
        :type hp_treshold: Tuple[int, int]

        :param speed_treshold: The generated Monster will have speed in this closed interval.
        Default value is [1, 100].
        :type speed_treshold: Tuple[int, int]

        :param max_dice: Maximum number of dice. Default value is 4.
        :type max_dice: int

        :param max_sides: Maximum number of sides. Default value is 8.
        :type max_sides: int

        :param max_effects: Maximum number of effects on each side. Default value is 3.
        :type max_effects: int

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param effect_type: If effect_type is passed as a parameter, the returned Dice sides will
        have effects of that type. Otherwise, each side will have effects of a random type.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Side.
        :rtype: Side
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        # Randomizing
        name = choice(self.team_names)

        members: List[Dice] = []

        for _ in range(team_members):
            member = self.get_random_monster(
                hp_treshold=hp_treshold,
                speed_treshold=speed_treshold,
                max_dice=max_dice,
                max_sides=max_sides,
                max_effects=max_effects,
                value_treshold=value_treshold,
                duration_treshold=duration_treshold,
                accuracy_treshold=accuracy_treshold,
                effect_type=effect_type,
                keyword_whitelist=keyword_whitelist,
                keyword_blacklist=keyword_blacklist,
            )

            if member.dice:
                members.append(member)

        team = Team(
            name=name,
            members=members,
        )

        return team

    def get_random_monster(
        self,
        hp_treshold: Tuple[int, int] = (1, 100),
        speed_treshold: Tuple[int, int] = (1, 100),
        max_dice: int = 4,
        max_sides: int = 8,
        max_effects: int = 3,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Monster:
        """
        Gets a random Monster with random Dice.

        :param hp_treshold: The generated Monster will have hp in this closed interval.
        Default value is [1, 100].
        :type hp_treshold: Tuple[int, int]

        :param speed_treshold: The generated Monster will have speed in this closed interval.
        Default value is [1, 100].
        :type speed_treshold: Tuple[int, int]

        :param max_dice: Maximum number of dice. Default value is 4.
        :type max_dice: int

        :param max_sides: Maximum number of sides. Default value is 8.
        :type max_sides: int

        :param max_effects: Maximum number of effects on each side. Default value is 3.
        :type max_effects: int

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param effect_type: If effect_type is passed as a parameter, the returned Dice sides will
        have effects of that type. Otherwise, each side will have effects of a random type.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Side.
        :rtype: Side
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        # Randomizing
        name = choice(self.monster_names)

        hp = randrange(hp_treshold[0], hp_treshold[1] + 1)
        speed = randrange(speed_treshold[0], speed_treshold[1] + 1)

        dice: List[Dice] = []
        chance = 1

        for _ in range(max_dice):
            if random() <= chance:
                one_dice = self.get_random_dice(
                    max_sides=max_sides,
                    max_effects=max_effects,
                    value_treshold=value_treshold,
                    duration_treshold=duration_treshold,
                    accuracy_treshold=accuracy_treshold,
                    effect_type=effect_type,
                    keyword_whitelist=keyword_whitelist,
                    keyword_blacklist=keyword_blacklist,
                )

                if one_dice.sides:
                    dice.append(one_dice)

                chance *= 0.5

        monster = Monster(
            global_id=uuid4(),
            name=name,
            hp=hp,
            max_hp=hp,
            speed=speed,
            mana=0,
            dice=dice,
        )

        return monster

    def get_random_dice(
        self,
        max_sides: int = 8,
        max_effects: int = 3,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Dice:
        """
        Gets a random Dice with random Sides.

        :param max_sides: Maximum number of sides. Default value is 8.
        :type max_sides: int

        :param max_effects: Maximum number of effects on each side. Default value is 3.
        :type max_effects: int

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param effect_type: If effect_type is passed as a parameter, the returned Dice sides will
        have effects of that type. Otherwise, each side will have effects of a random type.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Side.
        :rtype: Side
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        # Randomizing
        sides: List[Side] = []
        chance = 1

        for _ in range(max_sides):
            if random() <= chance:
                side = self.get_random_side(
                    max_effects=max_effects,
                    value_treshold=value_treshold,
                    duration_treshold=duration_treshold,
                    accuracy_treshold=accuracy_treshold,
                    effect_type=effect_type,
                    keyword_whitelist=keyword_whitelist,
                    keyword_blacklist=keyword_blacklist,
                )

                if side.effects:
                    sides.append(side)

                chance *= 0.8

        dice = Dice(sides)

        return dice

    def get_random_side(
        self,
        max_effects: int = 3,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Side:
        """
        Gets a random Side with effects of the same type.

        :param max_effects: Maximum number of effects. Default value is 3.
        :type max_effects: int

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param effect_type: If effect_type is passed as a parameter, the returned Side
        will have effects of that type. Otherwise, a random type will be chosen.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Side.
        :rtype: Side
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        if effect_type is None:
            effect_type = choice(list(EffectType))

        # Randomizing
        new_blacklist = deepcopy(keyword_blacklist)
        effects: List[Effect] = []
        chance = 1

        for _ in range(max_effects):
            if random() <= chance:
                effect = self.get_random_effect(
                    value_treshold=value_treshold,
                    duration_treshold=duration_treshold,
                    accuracy_treshold=accuracy_treshold,
                    effect_type=effect_type,
                    keyword_whitelist=keyword_whitelist,
                    keyword_blacklist=new_blacklist,
                )

                if effect:
                    effects.append(effect)
                    new_blacklist.append(effect.keyword)

                chance *= 0.5

        weight = randrange(1, 6)

        side = Side(effects, weight)

        return side

    def get_random_effect(
        self,
        value_treshold: Tuple[int, int] = (1, 100),
        duration_treshold: Tuple[int, int] = (1, 10),
        accuracy_treshold: Tuple[float, float] = (0.75, 1),
        max_immunity_effects: int = 3,
        effect_type: EffectType = None,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Effect:
        """
        Gets a random Effect.

        :param value_treshold: The generated Effect will have a value in this closed interval, unless it is
        Execute or Revive, which have a different treshold. Default value is [1, 100].
        :type value_treshold: Tuple[int, int]

        :param duration_treshold: The generated Effect will have a duration in this closed
        interval. Default value is [2, 10].
        :type duration_treshold: Tuple[int, int]

        :param accuracy_treshold: The generated Effect will have an accuracy in this closed
        interval. Default value is [0.75, 1].
        :type accuracy_treshold: Tuple[float, float]

        :param max_immunity_effects: Maximum number of immunity effects. Default value
        is 3.
        :type max_immunity_effects: int

        :param effect_type: If effect_type is passed as a parameter, the returned
        Effect will have the same type.
        :type effect_type: EffectType

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Effect.
        :rtype: Effect
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        valid_effects = deepcopy(self.all_effects)

        if effect_type:
            valid_effects = [
                effect for effect in valid_effects if effect.type == effect_type
            ]

        if keyword_whitelist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword in keyword_whitelist
            ]

        if keyword_blacklist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword not in keyword_blacklist
            ]

        # Randomizing
        if not valid_effects:
            return

        effect = choice(valid_effects)

        # Adjusting parameters
        if effect.keyword in [Keyword.EXECUTE]:
            effect.value = round(uniform(0.05, 0.1), 2)  # [5%, 25%]
        elif effect.keyword in [Keyword.REVIVE]:
            effect.value = round(uniform(0.05, 1), 2)  # [5%, 100%]
        else:
            effect.value = randrange(value_treshold[0], value_treshold[1] + 1)

        effect.duration = randrange(duration_treshold[0], duration_treshold[1] + 1)

        effect.accuracy = round(uniform(accuracy_treshold[0], accuracy_treshold[1]), 2)

        if effect.keyword in [Keyword.IMMUNITY]:
            effect: ImmunityEffect
            immunity_effects: List[Keyword] = []
            immunity_keyword_blacklist = [Keyword.IMMUNITY]
            chance = 1

            for _ in range(max_immunity_effects):
                if random() <= chance:
                    keyword = self.get_random_keyword(
                        keyword_blacklist=immunity_keyword_blacklist,
                    )

                    if keyword:
                        immunity_effects.append(keyword)
                        immunity_keyword_blacklist.append(keyword)

                    chance /= 2

            effect.effects = immunity_effects

        return effect

    def get_random_keyword(
        self,
        keyword_whitelist: List[Keyword] = None,
        keyword_blacklist: List[Keyword] = None,
    ) -> Keyword:
        """
        Gets a random Keyword.

        :param keyword_whitelist: If passed, only effects with these keywords will be
        elligible when generating the Effect.
        :type keyword_whitelist: List[Keyword]

        :param keyword_blacklist: If passed, only effects without these keywords will be
        elligible when generating the Effect.
        :type keyword_blacklist: List[Keyword]

        :return: Random Keyword.
        :rtype: Keyword
        """
        # Filtering
        keyword_whitelist = [] if keyword_whitelist is None else keyword_whitelist
        keyword_blacklist = [] if keyword_blacklist is None else keyword_blacklist

        valid_effects = deepcopy(self.all_effects)

        if keyword_whitelist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword in keyword_whitelist
            ]

        if keyword_blacklist:
            valid_effects = [
                effect
                for effect in valid_effects
                if effect.keyword not in keyword_blacklist
            ]

        # Randomizing
        if not valid_effects:
            return

        return choice(valid_effects).keyword
