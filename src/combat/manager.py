"""Combat Manager module."""

from enum import Enum
from random import random, shuffle
from typing import Dict, List, Literal, Tuple, TypedDict

from src.base.effect import Effect, EffectType
from src.base.entity import Entity
from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.side import Side
from src.base.triggers import Trigger
from src.logger.logger import Logger
from src.targeting.selectors.manager import SelectorManager


class OrderStrategy(Enum):
    """
    Strategy when definining monsters turn order in combat.

    * ``FASTER``: monsters act from highest to lowest speed
    * ``SET``: monsters act in the order they are provided
    * ``SHUFFLE``: monsters act in random order
    * ``SLOWER``: monsters act from lowest to highest speed
    """

    FASTER = "FASTER"
    SET = "SET"
    SHUFFLE = "SHUFFLE"
    SLOWER = "SLOWER"


class CombatStatus(TypedDict):
    """
    The combat's status.

    :var ALIVE: a list of teams with at least on monster with hp > 0.
    :vartype ALIVE: List[List[Monster]]

    :var DEFEATED: a list of teams with with all monsters with hp = 0.
    :vartype DEFEATED: List[List[Monster]]

    :var status: current combat status:
    :vartype status: Literal["DRAW", "ONGOING", "WINNER"]

    **Status:**
    * `"DRAW"`: the combat only has defeated teams
    * `"ONGOING"`: the combat may still continue
    * `"WINNER"`: the combat has only one alive team
    """

    ALIVE: List[List[Monster]]
    DEFEATED: List[List[Monster]]
    status: Literal["DRAW", "ONGOING", "WINNER"]


class CombatManager:
    """
    Combat Manager class.

    :var teams: Teams of characters or monsters that will fight each other.
    :vartype teams: List[List[Monster]]

    :var team_names: Teams of team names. If passed as a parameter, must have the same
    length as 'teams' parameter.
    :vartype team_names: str

    :var order_strategy: Strategy when definining monsters turn order in combat.
    Default value is OrderStrategy.FASTER.
    :vartype order_strategy: OrderStrategy

    :var logging: If the combat will be logged. Default value is True.
    :vartype logging: bool

    :var language: What language will be logged. Default value is "EN-US".
    :vartype language: Literal["EN-US", "PT-BR"]
    """

    def __init__(
        self,
        teams: List[List[Monster]] = None,
        team_names: List[str] = None,
        order_strategy: OrderStrategy = OrderStrategy.FASTER,
        logging: bool = True,
        language: Literal["EN-US", "PT-BR"] = "EN-US",
    ):
        self.round: int = 0
        self.turn: int = 0

        self.selector_manager = SelectorManager()
        self.logger = Logger(
            enabled=logging,
            language=language,
        )

        teams = [] if teams is None else teams
        team_names = [] if team_names is None else team_names

        if (teams) and (team_names) and (len(teams) != len(team_names)):
            raise AssertionError(
                "Parameters 'team' and 'team_names' must have the same length"
            )

        for idx, team in enumerate(teams):
            if team_names:
                team_name = team_names[idx]
            else:
                team_name = f"TEAM_{idx}"

            for monster in team:
                if monster.team_name is None:
                    monster.team_name = team_name

        self.teams = teams

        self.order_strategy = order_strategy
        self.order = []

        self.suffixes = {}
        self.add_suffixes()

    def _set_order(
        self,
    ) -> List[Monster]:
        """
        Returns the order in which characters and monsters will take action.

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        order: List[Monster] = [
            monster for team in self.teams for monster in team if monster.hp > 0
        ]

        if self.order_strategy == OrderStrategy.FASTER:
            order.sort(key=lambda x: x.speed, reverse=True)

        elif self.order_strategy == OrderStrategy.SLOWER:
            order.sort(key=lambda x: x.speed)

        elif self.order_strategy == OrderStrategy.SHUFFLE:
            shuffle(order)

        return order

    def count_names(self) -> Dict:
        """
        Returns a dictionary where each key is a name of a monster in combat and each
        value is the count of the monsters with this same name.
        """
        names = {}

        for team in self.teams:
            for monster in team:

                if monster.name not in names:
                    names[monster.name] = 1
                else:
                    names[monster.name] += 1

        return names

    def increase_character(self, character: str) -> Tuple[str, bool]:
        """
        Increases character by one:
        * If the character is not 'Z', returns the next character in the alphabet and
        False as a carry value.
        * If the character is 'Z', returns 'A' and True as a carry value.

        :param character: A single character.
        :type character: str

        :return: A (x, y) tuple where x is the increased character and y is a carry
        value.
        :rtype: Tuple[str, bool]
        """
        if len(character) != 1:
            raise ValueError("character length is not 1.")

        if character == "Z":
            return "A", True

        else:
            return chr(ord(character) + 1), False

    def increase_suffix(self, suffix: str) -> str:
        """
        Increases a suffix by one:
        * The last character in the suffix will be increased by one
        * If any character increase "carries over", than the character before that will
        also be increased by one

        Examples:
        * `increase_suffix("A")` = `"B"`
        * `increase_suffix("Z")` = `"AA"`
        * `increase_suffix("AZ")` = `"BA"`

        :param suffix: A monster suffix.
        :type suffix: str

        :return: The increased suffix.
        :rtype: str
        """
        if not suffix:
            return

        new_suffix = ""

        suffix: List[str] = [char for char in suffix]
        carry = True

        for char in reversed(suffix):
            if carry:
                new_char, carry = self.increase_character(char)
                new_suffix += new_char

            else:
                new_suffix += char

        new_suffix = "".join(reversed(new_suffix))
        if carry:
            new_suffix = "A" + new_suffix

        return new_suffix

    def add_suffixes(self):
        """
        Add suffixes to monsters to differentiate them in combat.
        """
        names = self.count_names()

        for team in self.teams:
            for monster in team:
                if monster.name is None:
                    continue

                # Updating combat suffixes
                if (monster.name not in self.suffixes) and (names[monster.name] > 1):
                    self.suffixes[monster.name] = "A"

                elif names[monster.name] > 1:
                    self.suffixes[monster.name] = self.increase_suffix(
                        self.suffixes[monster.name]
                    )

                # Setting monster suffix
                if (monster.suffix is None) and (monster.name in self.suffixes):
                    monster.suffix = self.suffixes[monster.name]

        return None

    def get_monster(self, monster_local_id: str) -> Monster:
        """
        Get a monster in the turn order.

        :param monster_local_id: Monster's unique local identifier.
        :type monster_local_id: str

        :return: A monster in the turn order.
        :rtype: Monster
        """
        if not monster_local_id:
            return None

        for monster in self.order:
            if monster.local_id == monster_local_id:
                return monster
        return None

    def get_team(
        self,
        monster: Monster = None,
        type: Literal["ALLIES", "ENEMIES", "SELF"] = "SELF",
    ) -> List[Monster]:
        """
        Get a list of monsters from the same team, relative to a monster.

        :param type: A type of team. Default value is "SELF".
        :type type: Literal["ALLIES", "ENEMIES", "SELF"]

        :param monster: The monster which the relative team will be returned.
        :type monster: Monster

        **Team types**
        * ``ALLIES``: all monsters from the same team, excluding itself
        * ``ENEMIES``: all monsters from different teams
        * ``SELF``: all monsters from the same team, including itself

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        selected: List[Monster] = []

        for team in self.teams:
            if (type == "SELF") and (team[0].team_name == monster.team_name):
                return [team_monster for team_monster in team]

            elif (type == "ALLIES") and (team[0].team_name == monster.team_name):
                return [
                    team_monster
                    for team_monster in team
                    if team_monster.local_id != monster.local_id
                ]

            elif (type == "ENEMIES") and (team[0].team_name != monster.team_name):
                selected.extend([team_monster for team_monster in team])

        return selected

    def get_team_status(
        self,
        monster: Monster = None,
        team: List[Monster] = None,
    ) -> Literal["ALIVE", "DEFEATED"]:
        """
        Returns the liveness status of a list of monsters:
        * ``ALIVE``: if at least one monster has their hp > 0
        * ``DEFEATED``: if all monsters have their hp = 0
        If a monster is passed, its team's liveness status will be returned.

        :param team: A monster.
        :type team: Monster

        :param team: A list of monsters.
        :type team: List[Monster]

        :return: Team status.
        :rtype: Literal["ALIVE", "DEFEATED"]
        """
        status: str = "DEFEATED"

        if (monster) and (not team):
            team = self.get_team(monster)

        for team_monster in team:
            if team_monster.hp > 0:
                status = "ALIVE"
                break

        return status

    def get_combat_status(self) -> CombatStatus:
        """
        Returns the current status of the combat.

        :return: The current combat status.
        :rtype: CombatStatus
        """
        teams_status = {
            "ALIVE": [],
            "DEFEATED": [],
        }

        for team in self.teams:
            team_status = self.get_team_status(team=team)
            teams_status[team_status].append(team)

        if len(teams_status["ALIVE"]) == 0:
            teams_status["status"] = "DRAW"

        elif len(teams_status["ALIVE"]) == 1:
            teams_status["status"] = "WINNER"

        else:
            teams_status["status"] = "ONGOING"

        return teams_status

    def add_monster(
        self,
        monster: Monster,
        team_name: str,
    ) -> None:
        """
        Adds a monster to combat.

        :param monster: The monster which will be added to combat.
        :type monster: Monster
        """
        monster.team_name = team_name

        for team in self.teams:
            if team[0].team_name == team_name:
                team.append(monster)
                break
        else:
            self.teams.append([monster])

        self.order = self._set_order()
        self.add_suffixes()

        return

    def remove_monster(
        self,
        monster: Monster,
    ) -> None:
        """
        Removes a monster from combat.

        :param monster: The monster which will be removed from combat.
        :type monster: Monster
        """
        empty_teams = []

        for team in self.teams:
            if monster in team:
                team.remove(monster)

            if not team:
                empty_teams.append(team)

        for team in empty_teams:
            self.teams.remove(team)

        if monster in self.order:
            self.order.remove(monster)

        return

    def check_deaths(self) -> None:
        """
        Checks and remove any dead monsters from combat.
        """
        for monster in self.order[:]:
            if monster.hp <= 0:
                self.logger.log(category="COMBAT", key="death", name=monster.name)
                self.remove_monster(monster)

        return

    def process_trigger(
        self,
        trigger: Trigger,
        target: Monster,
        source: Monster | None = None,
    ) -> None:
        """
        Activates all effects of a target monster that have the specified trigger type.
        The following triggers will invert the target and source monsters on
        activation:
        * BEING_ATTACKED

        :param trigger: A trigger.
        :type trigger: Trigger

        :param target: The monster which will have their effects activated.
        :type target: Monster

        :param source: An optional monster responsible for the effect being triggered.
        :type source: Monster
        """
        if not target:
            return

        for effect in target.effects[:]:

            # Invert target and source monsters
            if trigger == Trigger.BEING_ATTACKED:
                aux = target
                target = source
                source = aux

            if effect.trigger == trigger:
                effect_data = effect.activate(
                    target=target,
                    source=source,
                )

                # Logging triggered effect
                self.logger.log_effect_activation(
                    effect=effect,
                    source=source,
                    target=target,
                    **effect_data,
                )

        return

    def roll(self, entity: Entity) -> List[Side]:
        """
        Rolls all Entity's dice and returns the rolled Sides. The entity will be
        affected by Effects that triggers on dice roll.

        :param entity: An Entity.
        :type entity: Entity

        :return: A list containing the rolled Sides.
        :rtype: List[Side]
        """
        rolled = []

        for dice in entity.dice:
            rolled.append(dice.roll())

            # Procesing effects on dice roll
            self.process_trigger(
                Trigger.ROLL,
                target=entity,
            )

        return rolled

    def execute_effect(
        self,
        effect: Effect,
        source: Entity,
        target: Entity,
        check_can_act: bool = True,
        check_accuracy: bool = True,
    ) -> bool:
        """
        Executes an Effect through a series of checks. If the Effect is persistent, it
        will be applied to the target.

        :param effect: An Effect.
        :type effect: Effect

        :param source: The Entity object where the effect is from.
        :type source: Entity

        :param target: An Entity object which the effect will be applied.
        :type target: Entity

        :param check_can_act: If True, a check if the source can act will be done
        before trying do activate the Effect. Default value is True.
        :type check_can_act: bool

        :param check_accuracy: If True, an accuracy check will be done before
        trying do activate the Effect. Default value is True.
        :type check_accuracy: bool

        :return: If the effect was executed.
        :rtype: bool
        """
        # Check can act
        if (check_can_act) and (not source.can_act()):
            return False

        # Check accuracy
        if check_accuracy:
            accuracy = effect.accuracy

            # Blind check
            blinded = source.get_effect(Keyword.BLIND)

            if blinded and source != target:
                accuracy -= blinded.value

            if random() >= accuracy:
                self.logger.log(
                    category="COMBAT",
                    key="miss",
                    name=source.name,
                )
                return False

        # Persistent effects
        if effect.persistent:
            effect_data = target.apply_effect(
                effect,
                source=source,
            )

        # Instant effects
        else:
            effect_data = effect.activate(
                source=source,
                target=target,
            )

        # Log effect execution
        self.logger.log_effect_execution(
            effect=effect,
            source=source,
            target=target,
            **effect_data,
        )

        # Log effect removals
        for removed_effect in effect_data.get("removed_effects", []):
            self.logger.log_effect_removal(
                effect=effect,
                source=source,
                target=target,
                removed_effect=removed_effect,
            )

        # Procesing effects on being attacked
        if effect.type == EffectType.OFFENSIVE:
            self.process_trigger(
                Trigger.BEING_ATTACKED,
                source=source,
                target=target,
            )

        return True

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
        self.order = self._set_order()
        self.current_monster = self.order[0]
        return

    def start_round(self) -> None:
        """Start the current round."""
        self.round += 1
        self.turn = 0
        return

    def start_turn(self) -> None:
        """
        Start the current monster's turn. The entity will be affected by Effects that
        triggers on turn start.
        """
        self.turn += 1

        # Procesing effects on turn start
        self.process_trigger(
            Trigger.TURN_START,
            target=self.current_monster,
        )

        return

    def take_action(
        self,
        monster: Monster,
    ) -> None:
        """
        Takes action automatically for a monster:
        * Their dice will be rolled
        * Each rolled side will have their targets determined
        * Each effect of the rolled side will be applied onto every target

        :param monster: The monster which will have its actions taken.
        :type monster: Monster
        """
        sides = self.roll(monster)

        allies = self.get_team(monster, "ALLIES")
        enemies = self.get_team(monster, "ENEMIES")

        for side in sides:
            targets = self.selector_manager.get_targets(
                side=side,
                source=monster,
                allies=allies,
                enemies=enemies,
                k=1,
                difficulty=monster.difficulty,
            )

            for target in targets:
                for effect in side.effects:
                    self.execute_effect(
                        effect=effect,
                        source=monster,
                        target=target,
                    )

        return

    def take_turn(self) -> bool:
        """
        The current monster takes its turn, based on its control type. If the monster
        is under any FREEZE, SLEEP or STUN effects, it won't take its turn.

        :return: If the turn was taken.
        :rtype: bool
        """
        for keyword in [
            Keyword.FREEZE,
            Keyword.SLEEP,
            Keyword.STUN,
        ]:
            effect = self.current_monster.get_effect(keyword)

            if effect:
                self.logger.log_effect_activation(
                    effect=effect,
                    source=None,
                    target=self.current_monster,
                )
                return False

        if self.current_monster.control_type == ControlType.AI:
            self.take_action(self.current_monster)

        elif self.current_monster.control_type == ControlType.PLAYER:
            raise NotImplementedError

        return True

    def end_turn(self) -> Dict:
        """
        End the current monster's turn. The entity will be affected by Effects that
        triggers on turn end. Then, all effects on the current monsters will be
        decayed and removed if their duration are <= 0.

        :return: A dictionary containing objects that were affected by the turn ending.
        :rtype: Dict

        **Return keys**
        * ``removed_effects``: a list of effects that were removed from the current
        monster
        """
        # Procesing effects on turn end
        self.process_trigger(
            Trigger.TURN_END,
            target=self.current_monster,
        )

        # Decaying and removing effects
        idx_removed_effects = []

        for idx, effect in enumerate(self.current_monster.effects):
            effect.duration -= 1
            effect.value -= effect.decay

            if effect.duration <= 0:
                idx_removed_effects.append(idx)

        removed_effects = [
            effect
            for idx, effect in enumerate(self.current_monster.effects)
            if idx in idx_removed_effects
        ]
        self.current_monster.effects = [
            effect
            for idx, effect in enumerate(self.current_monster.effects)
            if idx not in idx_removed_effects
        ]

        return {
            "removed_effects": removed_effects,
        }

    def next_turn(self) -> None:
        """Sets up the next turn in the turn order."""

        idx_monster: int = None
        for idx, monster in enumerate(self.order):
            if monster == self.current_monster:
                idx_monster = idx
                break

        while True:
            idx_monster += 1

            monster = self.order[idx_monster % len(self.order)]

            if monster.hp > 0:
                self.current_monster = monster
                break

        return

    def end_round(self) -> None:
        """End the current round."""
        return

    def end_combat(self) -> None:
        """End combat between teams of monsters."""
        return

    def run(self) -> Dict:
        """
        Runs combat until only one team remains alive.
        """
        self.start_combat()
        self.check_deaths()

        while self.get_combat_status()["status"] == "ONGOING":
            self.start_round()
            self.check_deaths()

            self.logger.log_round(self.round)
            self.logger.log_teams(self.teams)

            for monster in self.order:
                self.current_monster = monster

                self.start_turn()
                self.check_deaths()

                if monster.hp > 0:
                    self.logger.log(
                        category="COMBAT", key="turn", name=self.current_monster.name
                    )
                    self.take_turn()
                    self.check_deaths()

                self.end_turn()
                self.check_deaths()

                combat_status = self.get_combat_status()
                if combat_status["status"] == "DRAW":
                    self.logger.log(category="COMBAT", key="draw")
                    break

                elif combat_status["status"] == "WINNER":
                    self.logger.log(
                        category="COMBAT",
                        key="winner",
                        team_name=combat_status["ALIVE"][0][0].team_name,
                    )
                    break

            self.end_round()
            self.check_deaths()

        self.end_combat()

        return self.get_combat_status()
