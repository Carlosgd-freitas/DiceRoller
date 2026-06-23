"""Combat Manager module."""

from __future__ import annotations

from enum import Enum
from math import inf
from random import shuffle
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, TypedDict

from src.base.keywords import Keyword
from src.base.manager import Manager
from src.base.monster import ControlType, Monster
from src.base.triggers import Trigger
from src.combat.effects import EffectManager
from src.combat.suffixes import SuffixManager
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.targeting.selectors.manager import SelectorManager

if TYPE_CHECKING:
    from src.combat.team import Team
    from src.systems.settings import Settings


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


class CombatData(TypedDict):
    """
    Combat Data.

    :var round: combat round number.
    :vartype round: int

    :var teams: teams of monsters in combat.
    :vartype teams: List[Team]

    :var turn: combat turn number.
    :vartype turn: int
    """

    round: int
    teams: List[Team]
    turn: int


class CombatStatus(TypedDict):
    """
    The combat's status.

    :var ALIVE: a list of teams with at least one alive monster.
    :vartype ALIVE: List[Team]

    :var DEFEATED: a list of teams with with all dead monsters.
    :vartype DEFEATED: List[Team]

    :var status: current combat status.
    :vartype status: Literal["DRAW", "ONGOING", "WINNER"]

    **Status:**
    * `"DRAW"`: the combat only has defeated teams
    * `"ONGOING"`: the combat may still continue
    * `"WINNER"`: the combat has only one alive team
    """

    ALIVE: List[Team]
    DEFEATED: List[Team]
    status: Literal["DRAW", "ONGOING", "WINNER"]


class CombatManager(Manager):
    """
    CombatManager class.

    :var settings: Game settings.
    :vartype settings: Settings

    :var teams: Teams of characters or monsters that will fight each other.
    :vartype teams: List[Team]

    :var order_strategy: Strategy when definining monsters turn order in combat.
    Default value is OrderStrategy.FASTER.
    :vartype order_strategy: OrderStrategy

    :var logging: If logging is enabled. Default value is True.
    :vartype logging: bool
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        settings: Settings,
        teams: List[Team] = None,
        order_strategy: OrderStrategy = OrderStrategy.FASTER,
        logging: bool = True,
    ):
        # Initialization
        logger = CombatLogger(enabled=logging)

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger

        # Effect Management
        self.effect_manager = EffectManager(
            settings,
            logging,
        )

        # Suffix Management
        self.suffix_manager = SuffixManager()

        # Target Selection Management
        self.selector_manager = SelectorManager()

        # Team Management
        self.teams = [] if teams is None else teams

        # Turn Management
        self.round: int = 1
        self.turn: int = 1
        self.order_strategy = order_strategy
        self.order: List[Monster] = []
        self.current_monster: Monster = None

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language, _messages: Dict = None):
        """
        Changes the Manager language.

        :var language: A Language.
        :vartype language: Language

        :var _messages: Messages loaded from a locale module.
        :vartype _messages: Dict
        """
        self.logger.change_language(language, _messages)
        _messages = self.logger._messages

        self.effect_manager.change_language(language, _messages)

        self.update_teams()

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled
        self.effect_manager.toggle_logging(enabled)

    def update_teams(self):
        """
        Updates teams's members with:
        * parameters that depends on a locale (name, description, etc.)
        * suffixes
        """
        self.suffix_manager.suffixes = {}

        for team in self.teams:
            for monster in team.members:
                name = self.logger.get_message(
                    namespace="monsters",
                    message_group=monster.global_id,
                    key="name",
                )

                description = self.logger.get_message(
                    namespace="monsters",
                    message_group=monster.global_id,
                    key="description",
                )

                monster.update_locale_params(name, description)

        self.suffix_manager.add_suffixes(self.teams)

    def get_combat_data(self) -> CombatData:
        """
        Gets the current combat data.

        :return: Combat data.
        :rtype: CombatData
        """
        return {
            "round": self.round,
            "teams": self.teams,
            "turn": self.turn,
        }

    def set_combat_data(self, combat_data: CombatData):
        """
        Sets combat data.

        :var combat_data: Combat data.
        :vartype combat_data: CombatData
        """
        self.__dict__.update(combat_data)
        self.update_teams()

    # =========================================================================
    # Team Management
    # =========================================================================

    def get_team(
        self,
        member: Monster = None,
        name: str = None,
    ) -> Team:
        """
        Returns a team.

        :param member: A member of the team.
        :type member: Monster

        :param name: The name of the team.
        :type name: str

        :return: A team.
        :rtype: Team
        """
        for team in self.teams:
            if (name) and (team.name == name):
                return team

            elif (member) and (member in team.members):
                return team

        return

    def get_allies(
        self,
        monster: Monster,
    ) -> List[Monster]:
        """
        Returns all allies of a monster.

        :param monster: A monster.
        :type monster: Monster

        :return: A list of monster allies.
        :rtype: List[Monster]
        """
        team = self.get_team(member=monster)

        return [
            team_monster for team_monster in team.members if team_monster != monster
        ]

    def get_enemies(
        self,
        monster: Monster,
    ) -> List[Monster]:
        """
        Returns all enemies of a monster.

        :param monster: A monster.
        :type monster: Monster

        :return: A list of monster enemies.
        :rtype: List[Monster]
        """
        enemies = []
        monster_team = self.get_team(member=monster)

        for team in self.teams:
            if team != monster_team:
                enemies.extend(team.members)

        return enemies

    def add_monster(
        self,
        monster: Monster,
        team: Team = None,
        team_name: str = None,
    ) -> None:
        """
        Adds a monster to combat.

        :param monster: The monster which will be added to combat.
        :type monster: Monster

        :param team: The team that the monster will be added to.
        :type team: Team

        :param team_name: The name of the team that the monster will be added to.
        :type team_name: str
        """
        for self_team in self.teams:
            if (team_name) and (self_team.name == team_name):
                self_team.members.append(monster)

            elif (team) and (self_team == team):
                self_team.members.append(monster)

        self.update_teams()

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
        for team in self.teams:
            if monster in team.members:
                team.members.remove(monster)

        return

    # =========================================================================
    # Turn Management
    # =========================================================================

    def get_turn_order(self) -> List[Monster]:
        """
        Returns the order in which monsters will take action.

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        order: List[Monster] = [
            monster
            for team in self.teams
            for monster in team.members
            if monster.is_alive()
        ]

        if self.order_strategy == OrderStrategy.FASTER:
            order.sort(key=lambda x: x.get_effective_speed(), reverse=True)

        elif self.order_strategy == OrderStrategy.SLOWER:
            order.sort(key=lambda x: x.get_effective_speed())

        elif self.order_strategy == OrderStrategy.SHUFFLE:
            shuffle(order)

        return order

    def set_order(self, order_strategy: OrderStrategy):
        """
        Sets the order in which monsters will take action.

        :param order_strategy: Strategy when definining monsters turn order in combat.
        :type order_strategy: OrderStrategy
        """
        self.order_strategy = order_strategy
        self.order = self.get_turn_order()

    def is_round_start(self) -> bool:
        """
        Returns if the combat is currently on round start.

        :return: If the combat is in round start or not.
        :rtype: bool
        """
        return all([not monster.turn_taken for monster in self.order])

    def is_round_end(self) -> bool:
        """
        Returns if the combat is currently on round end.

        :return: If the combat is in round end or not.
        :rtype: bool
        """
        return all([monster.turn_taken for monster in self.order])

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
        self.set_order(self.order_strategy)

        for monster in self.order:
            monster.turn_taken = False

            # Procesing effects on combat start
            if monster.in_combat and monster.is_alive():
                self.effect_manager.process_trigger(
                    Trigger.COMBAT_START,
                    target=monster,
                )

        self.current_monster = self.order[0]

        return

    def start_round(self) -> None:
        """Start the current round."""
        self.set_order(self.order_strategy)

        for monster in self.order:
            # Procesing effects on round start
            if monster.in_combat and monster.is_alive():
                self.effect_manager.process_trigger(
                    Trigger.ROUND_START,
                    target=monster,
                )

        self.current_monster = self.order[0]

        return

    def start_turn(self) -> None:
        """
        Start the current monster's turn. The entity will be affected by Effects that
        triggers on turn start.
        """
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

        allies = self.get_allies(monster)
        enemies = self.get_enemies(monster)

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
        self.current_monster.turn_taken = True

        for keyword in [
            Keyword.FREEZE,
            Keyword.SLEEP,
            Keyword.STUN,
        ]:
            effect = self.current_monster.get_effect(keyword)

            if effect:
                self.effect_manager.logger.log_effect_activation(
                    effect=effect,
                    source=self.current_monster,
                    target=None,
                    fail=keyword.name.lower(),
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
        to_remove = []
        removed_effects = []

        for effect in self.current_monster.effects:
            if effect.duration != inf:
                effect.duration -= 1

                # Procesing effects on duration decay
                self.effect_manager.process_trigger(
                    Trigger.DURATION_DECAY,
                    target=self.current_monster,
                )

            if effect.decay:
                effect.value -= effect.decay

            if effect.duration <= 0:
                to_remove.append(effect.keyword)

        for keyword in to_remove:
            # Procesing effects on removal
            self.effect_manager.process_trigger(
                Trigger.REMOVE,
                target=self.current_monster,
            )

            removed_effect = self.current_monster.remove_effect(keyword)
            removed_effects.append(removed_effect)

        self.turn += 1

        return {
            "removed_effects": removed_effects,
        }

    def next_turn(self):
        """Sets up the next turn in the turn order."""
        self.set_order(self.order_strategy)

        for monster in self.order:
            if (monster != self.current_monster) and (not monster.turn_taken):
                self.current_monster = monster
                break

        return

    def end_round(self) -> None:
        """End the current round."""
        for monster in self.order:
            # Clearing turn taken flags
            monster.turn_taken = False

            # Procesing effects on round end
            if monster.in_combat and monster.is_alive():
                self.effect_manager.process_trigger(
                    Trigger.ROUND_END,
                    target=monster,
                )

        self.round += 1

        return

    def end_combat(self) -> None:
        """End combat between teams of monsters."""
        # Procesing effects on combat end
        for monster in self.order:
            if monster.in_combat and monster.is_alive():
                self.effect_manager.process_trigger(
                    Trigger.COMBAT_END,
                    target=monster,
                )

        return

    # =========================================================================
    # Combat Management
    # =========================================================================

    def check_deaths(self) -> None:
        """
        Checks deaths from monsters in combat and logs their deaths. Dead monsters will
        be affected by Effects that triggers on death.
        """
        for monster in self.order[:]:
            if monster.in_combat and not monster.is_alive():
                team = self.get_team(member=monster)
                team.status = team.get_status()

                self.logger.log_monster_death(monster)

                # Updating monster on death
                monster.effects = []
                monster.in_combat = False

                # Procesing effects on death
                self.effect_manager.process_trigger(
                    Trigger.DEATH,
                    target=monster,
                )

        return

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
            team.status = team.get_status()
            teams_status[team.status].append(team)

        if len(teams_status["ALIVE"]) == 0:
            teams_status["status"] = "DRAW"

        elif len(teams_status["ALIVE"]) == 1:
            teams_status["status"] = "WINNER"

        else:
            teams_status["status"] = "ONGOING"

        return teams_status

    def check_combat_status(self) -> None:
        """
        Checks and returns the current combat status. If the combat is over, an
        appropiate message will be logged.
        """
        combat_status = self.get_combat_status()

        if combat_status["status"] == "DRAW":
            self.logger.log(namespace="combat", message_group="COMBAT", key="draw")

        elif combat_status["status"] == "WINNER":
            self.logger.log(
                namespace="combat",
                message_group="COMBAT",
                key="winner",
                team_name=combat_status["ALIVE"][0].name,
            )

        return combat_status

    def _run_step(self, step: Callable, **kwargs):
        """Runs a step of combat, check deaths and return the combat status."""
        step(**kwargs)
        self.check_deaths()
        return self.check_combat_status()

    def run(self) -> Dict:
        """
        Runs combat until only one team remains alive.
        """
        # Combat Start
        combat_status = self._run_step(self.start_combat)

        while combat_status["status"] == "ONGOING":
            # Round Start
            if self.is_round_start():
                if self.round == 1 or self.settings.end_turn_ai_monsters == "AUTO":
                    start_line_break = True
                else:
                    start_line_break = False

                self.logger.log_round(
                    self.round,
                    start_line_break,
                )

                combat_status = self._run_step(self.start_round)
                if combat_status["status"] != "ONGOING":
                    break

            # Turn Start
            if (self.settings.end_turn_ai_monsters == "MANUAL") and (
                not self.is_round_start()
            ):
                start_line_break = False
            else:
                start_line_break = True

            self.logger.log_turn_start(
                self.current_monster,
                start_line_break,
            )
            self.logger.log_teams(self.teams)

            combat_status = self._run_step(self.start_turn)
            if combat_status["status"] != "ONGOING":
                break

            # Take Turn Action
            if self.current_monster.is_alive():
                combat_status = self._run_step(self.take_turn)

                if combat_status["status"] != "ONGOING":
                    break

            # Turn End
            combat_status = self._run_step(self.end_turn)
            if combat_status["status"] != "ONGOING":
                break

            if self.settings.end_turn_ai_monsters == "MANUAL":
                self.logger.input("")

            # Next Turn
            self.next_turn()

            # Round End
            if self.is_round_end():
                combat_status = self._run_step(self.end_round)
                if combat_status["status"] != "ONGOING":
                    break

        # Combat end
        self.end_combat()

        return combat_status
