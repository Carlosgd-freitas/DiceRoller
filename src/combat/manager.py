"""Combat Manager module."""

from enum import Enum
from random import shuffle
from typing import Dict, List, Literal, TypedDict

from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.triggers import Trigger
from src.combat.effects import EffectManager
from src.combat.suffixes import SuffixManager
from src.logger.combat_logger import CombatLogger
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
        # Logger
        self.logger = CombatLogger(
            enabled=logging,
            language=language,
        )

        # Effect Management
        self.effect_manager = EffectManager(logger=self.logger)

        # Team Management
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

        # Turn Management
        self.round: int = 0
        self.turn: int = 0
        self.order_strategy = order_strategy
        self.order = []

        # Suffix Management
        self.suffix_manager = SuffixManager()
        self.suffix_manager.add_suffixes(self.teams)

        # Target Selection Management
        self.selector_manager = SelectorManager()

    def _set_order(
        self,
    ) -> List[Monster]:
        """
        Returns the order in which characters and monsters will take action.

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        order: List[Monster] = [
            monster for team in self.teams for monster in team if monster.is_alive()
        ]

        if self.order_strategy == OrderStrategy.FASTER:
            order.sort(key=lambda x: x.speed, reverse=True)

        elif self.order_strategy == OrderStrategy.SLOWER:
            order.sort(key=lambda x: x.speed)

        elif self.order_strategy == OrderStrategy.SHUFFLE:
            shuffle(order)

        return order

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
            if team_monster.is_alive():
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
        self.suffix_manager.add_suffixes(self.teams)

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
            if not monster.is_alive():
                self.logger.log(category="COMBAT", key="death", name=monster.name)
                self.remove_monster(monster)

        return

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
        self.effect_manager.process_trigger(
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
        sides = self.effect_manager.roll(monster)

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
                    self.effect_manager.execute_effect(
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
        self.effect_manager.process_trigger(
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

            for monster in self.order:
                self.current_monster = monster

                self.logger.log_turn_start(self.current_monster)
                self.logger.log_teams(self.teams)

                self.start_turn()
                self.check_deaths()

                if monster.is_alive():
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
