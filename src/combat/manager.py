"""Combat Manager module."""

from __future__ import annotations

from copy import deepcopy
from math import inf
from random import shuffle
from typing import TYPE_CHECKING, Callable, Dict, List, Literal, TypedDict

from src.base.color import color_string
from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.triggers import Trigger
from src.combat.effects import EffectManager
from src.combat.order_strategy import OrderStrategy
from src.combat.player_actions import CombatPlayerActionsMenu
from src.combat.suffixes import SuffixManager
from src.combat.team_manager import TeamManager
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.systems.manager import Manager
from src.systems.targeting.selectors.manager import SelectorManager

if TYPE_CHECKING:
    from src.base.team import Team
    from src.systems.settings import Settings


class CombatData(TypedDict):
    """
    Combat Data.

    :var order_strategy: Strategy when definining monsters turn order in combat.
    :vartype order_strategy: OrderStrategy

    :var round: combat round number.
    :vartype round: int

    :var teams: teams of monsters in combat.
    :vartype teams: List[Team]

    :var turn: combat turn number.
    :vartype turn: int
    """

    order_strategy: OrderStrategy
    round: int
    teams: List[Team]
    turn: int


def are_combat_data_equivalent(
    combat_data_1: CombatData, combat_data_2: CombatData
) -> bool:
    """
    Compares two combat data and returns if they are equivalent.

    :param combat_data_1: Combat data for comparison.
    :type v: CombatData

    :param combat_data_2: Combat data for comparison.
    :type combat_data_2: CombatData

    :return: If the combat data are equivalent.
    :rtype: bool
    """
    return (
        isinstance(combat_data_1, dict)
        and isinstance(combat_data_2, dict)
        and combat_data_1.get("order_strategy") == combat_data_2.get("order_strategy")
        and len(combat_data_1.get("teams", [])) == len(combat_data_2.get("teams", []))
        and all(
            [
                team_1.is_equivalent(team_2)
                for team_1, team_2 in zip(
                    combat_data_1.get("teams", []),
                    combat_data_2.get("teams", []),
                    strict=True,
                )
            ]
        )
    )


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

    :var softlock_limit: In round ends, if the number of sequentially sotflock states
    reach this limit, the combat ends in a draw. Default value is 3.
    :vartype softlock_limit: int
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
        softlock_limit: int = 3,
    ):
        # Initialization
        logger = CombatLogger(
            enabled=logging,
            language=settings.language,
        )

        super().__init__(
            logger,
            settings,
        )

        self.logger: CombatLogger
        self.previous_combat_data = None

        # Effect Management
        self.effect_manager = EffectManager(settings, logging)

        # Softlock Management
        self.softlock_count = 0
        self.softlock_limit = softlock_limit

        # Suffix Management
        self.suffix_manager = SuffixManager()

        # Target Selection Management
        self.selector_manager = SelectorManager()

        # Team Management
        self.teams = [] if teams is None else teams
        self.team_manager = TeamManager()
        self.update_teams()

        # Turn Management
        self.round: int = 1
        self.turn: int = 1
        self.order_strategy = order_strategy
        self.order: List[Monster] = []
        self.current_monster: Monster = None

        # Player actions
        self.player_actions_menu = CombatPlayerActionsMenu(
            settings,
            logging,
            self.teams,
        )

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
        self.update_teams()

        # Managers
        self.effect_manager.change_language(language, _messages)

        # Menus
        self.player_actions_menu.change_language(language, _messages)

    def toggle_logging(self, enabled: bool):
        """
        Enables or disables the Manager logging.

        :var enabled: If the Manager logging is enabled or disabled.
        :vartype enabled: bool
        """
        self.logger.enabled = enabled

        # Managers
        self.effect_manager.toggle_logging(enabled)

        # Menus
        self.player_actions_menu.toggle_logging(enabled)

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
            "order_strategy": self.order_strategy,
            "round": self.round,
            "teams": deepcopy(self.teams),
            "turn": self.turn,
        }

    def set_combat_data(self, combat_data: CombatData):
        """
        Sets combat data.

        :var combat_data: Combat data.
        :vartype combat_data: CombatData
        """
        for attribute in [
            "order_strategy",
            "round",
            "turn",
            "teams",
        ]:
            if combat_data.get(attribute) is not None:
                setattr(self, attribute, deepcopy(combat_data[attribute]))

        self.update_teams()

    def check_softlock(self) -> bool:
        """
        Checks and returns if the combat is currently softlocked.

        :return: If the combat is currently softlocked.
        :rtype: bool
        """
        current_combat_data = self.get_combat_data()

        if are_combat_data_equivalent(current_combat_data, self.previous_combat_data):
            self.softlock_count += 1
        else:
            self.softlock_count = 0

        return self.softlock_count >= self.softlock_limit

    # =========================================================================
    # Team Management
    # =========================================================================

    def add_monster(
        self,
        monster: Monster,
        team: Team = None,
    ) -> None:
        """
        Adds a monster to combat.

        :param monster: The monster which will be added.
        :type monster: Monster

        :param team: The team that the monster will be added to.
        :type team: Team

        :param team_name: The name of the team that the monster will be added to.
        :type team_name: str
        """
        self.team_manager.add_monster(
            monster=monster,
            teams=self.teams,
            team=team,
        )

        self.update_teams()

        return

    def remove_monster(
        self,
        monster: Monster,
    ) -> None:
        """
        Removes a monster from combat.

        :param monster: The monster which will be removed.
        :type monster: Monster
        """
        self.team_manager.remove_monster(
            monster=monster,
            teams=self.teams,
        )

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

        self.previous_combat_data = self.get_combat_data()

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

    def ai_controlled_action(
        self,
        monster: Monster,
    ) -> None:
        """
        Takes action for an AI controlled monster:
        * Their dice will be rolled
        * Each rolled side will have their targets determined
        * Each effect of the rolled side will be applied onto every target

        :param monster: The monster which will have its actions taken.
        :type monster: Monster
        """
        sides = self.effect_manager.roll(monster)
        self.logger.log_roll_dice(monster, sides)

        allies = self.team_manager.get_allies(monster, self.teams)
        enemies = self.team_manager.get_enemies(monster, self.teams)

        for side in sides:
            targets = self.selector_manager.get_targets(
                side=side,
                source=monster,
                allies=allies,
                enemies=enemies,
                k=1,
                ai_level=monster.ai_level,
            )

            for target in targets:
                for effect in side.effects:
                    self.effect_manager.execute_effect(
                        effect=effect,
                        source=monster,
                        target=target,
                    )

        return

    def player_controlled_action(
        self,
        monster: Monster,
    ) -> None:
        """
        Allows a player controlled monster to take action.

        :param monster: The monster which will have its actions taken.
        :type monster: Monster
        """
        self.player_actions_menu.open(monster, self.teams)

        # Syncing loggers
        if self.player_actions_menu.logger.language != self.logger.language:
            self.change_language(
                self.player_actions_menu.logger.language,
                self.player_actions_menu.logger._messages,
            )

        if self.player_actions_menu.logger.enabled != self.logger.enabled:
            self.toggle_logging(self.player_actions_menu.logger.enabled)

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
            self.ai_controlled_action(self.current_monster)

        elif self.current_monster.control_type == ControlType.PLAYER:
            self.player_controlled_action(self.current_monster)

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

        # Applying delta and removing effects
        to_remove = []
        removed_effects = []

        for effect in self.current_monster.effects:
            if effect.duration != inf:
                effect.duration -= 1

                # Processing only duration trigger effects
                if effect.trigger == Trigger.DURATION_DECAY:
                    effect_data = effect.activate(
                        source=None,
                        target=self.current_monster,
                    )

                    # Logging triggered effect
                    self.logger.log_effect_activation(
                        effect=effect,
                        source=None,
                        target=self.current_monster,
                        **effect_data,
                    )

            if effect.delta:
                if effect.delta.flat:
                    effect.value.flat += effect.delta.flat
                if effect.delta.percent:
                    effect.value.flat += effect.value.flat * effect.delta.percent

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

        # Softlock check
        self.check_softlock()
        self.previous_combat_data = self.get_combat_data()

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
                team = self.team_manager.get_team(member=monster, teams=self.teams)
                team.status = team.get_status()

                self.logger.log_monster_death(monster)

                # Updating monster on death
                monster.effects = [
                    effect for effect in monster.effects if not effect.removable
                ]
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

        if (
            self.softlock_count >= self.softlock_limit
            or len(teams_status["ALIVE"]) == 0
        ):
            teams_status["status"] = "DRAW"

        elif len(teams_status["ALIVE"]) == 1:
            teams_status["status"] = "WINNER"

        else:
            teams_status["status"] = "ONGOING"

        return teams_status

    def check_combat_status(self) -> CombatStatus:
        """
        Checks and returns the current combat status. If the combat is over, an
        appropiate message will be logged.

        :return: The current combat status.
        :rtype: CombatStatus
        """
        combat_status = self.get_combat_status()

        if combat_status["status"] == "DRAW":
            self.logger.log(namespace="combat", message_group="COMBAT", key="draw")

        elif combat_status["status"] == "WINNER":
            team_name = combat_status["ALIVE"][0].name
            team_name = color_string(team_name, intensity="BRIGHT")

            self.logger.log(
                namespace="combat",
                message_group="COMBAT",
                key="winner",
                team_name=team_name,
            )

        return combat_status

    def _run_step(self, step: Callable, **kwargs) -> CombatStatus:
        """
        Runs a step of combat, check deaths and return the combat status.

        :param step: A combat step method.
        :type step: Callable

        :return: The current combat status.
        :rtype: CombatStatus
        """
        step(**kwargs)
        self.check_deaths()
        combat_status = self.check_combat_status()
        return combat_status

    def run(self) -> CombatStatus:
        """
        Runs combat until it is finished.

        :return: The final combat status.
        :rtype: CombatStatus
        """
        # Combat Start
        combat_status = self._run_step(self.start_combat)

        while combat_status["status"] == "ONGOING":
            # Round Start
            if self.is_round_start():
                if self.round == 1 or self.settings.monster_end_turn == "AUTO":
                    start_line_break = True
                else:
                    start_line_break = False

                self.logger.log_round_start(
                    self.round,
                    start_line_break,
                )

                combat_status = self._run_step(self.start_round)
                if combat_status["status"] != "ONGOING":
                    break

            # Turn Start
            if (self.settings.monster_end_turn == "MANUAL") and (
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

            if (
                self.settings.monster_end_turn == "MANUAL"
                and self.current_monster.control_type == ControlType.AI
            ):
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
