"""Combat Manager module."""

from __future__ import annotations

from enum import Enum
from random import shuffle
from typing import TYPE_CHECKING, Dict, List, Literal, TypedDict

from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.triggers import Trigger
from src.combat.effects import EffectManager
from src.combat.suffixes import SuffixManager
from src.locales.languages import Language
from src.logger.combat import CombatLogger
from src.logger.effects import EffectLogger
from src.targeting.selectors.manager import SelectorManager

if TYPE_CHECKING:
    from src.combat.team import Team


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


class CombatManager:
    """
    Combat Manager class.

    :var teams: Teams of characters or monsters that will fight each other.
    :vartype teams: List[Team]

    :var order_strategy: Strategy when definining monsters turn order in combat.
    Default value is OrderStrategy.FASTER.
    :vartype order_strategy: OrderStrategy

    :var logging: If the combat will be logged. Default value is True.
    :vartype logging: bool

    :var language: What language will be logged. Default value is Language.EN_US.
    :vartype language: Language
    """

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(
        self,
        teams: List[Team] = None,
        order_strategy: OrderStrategy = OrderStrategy.FASTER,
        logging: bool = True,
        language: Language = Language.EN_US,
    ):
        # Logger
        self.logger = CombatLogger(
            enabled=logging,
            language=language,
        )

        # Effect Management
        effect_logger = EffectLogger(
            enabled=logging,
            language=language,
        )
        self.effect_manager = EffectManager(logger=effect_logger)

        # Team Management
        self.teams = [] if teams is None else teams

        # Turn Management
        self.round: int = 1
        self.turn: int = 1
        self.order_strategy = order_strategy
        self.order: List[Monster] = []
        self.current_monster: Monster = None

        # Suffix Management
        self.suffix_manager = SuffixManager()
        self.suffix_manager.add_suffixes(self.teams)

        # Target Selection Management
        self.selector_manager = SelectorManager()

    # =========================================================================
    # Utility
    # =========================================================================

    def change_language(self, language: Language):
        """
        Changes the combat's language.

        :var language: A Language.
        :vartype language: Language
        """
        self.logger.change_language(language)
        self.effect_manager.logger._messages = self.logger._messages

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
            order.sort(key=lambda x: x.speed, reverse=True)

        elif self.order_strategy == OrderStrategy.SLOWER:
            order.sort(key=lambda x: x.speed)

        elif self.order_strategy == OrderStrategy.SHUFFLE:
            shuffle(order)

        return order

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
        self.order = self.get_turn_order()
        self.current_monster = self.order[0]
        return

    def start_round(self) -> None:
        """Start the current round."""
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
        for keyword in [
            Keyword.FREEZE,
            Keyword.SLEEP,
            Keyword.STUN,
        ]:
            effect = self.current_monster.get_effect(keyword)

            if effect:
                self.effect_manager.logger.log_effect_activation(
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

        self.turn += 1

        return {
            "removed_effects": removed_effects,
        }

    def next_turn(self) -> None:
        """Sets up the next turn in the turn order."""

        # Getting the current monster
        idx_monster: int = None
        for idx, monster in enumerate(self.order):
            if monster == self.current_monster:
                idx_monster = idx
                break

        # Getting the next monster
        if idx_monster + 1 < len(self.order):
            self.current_monster = self.order[idx_monster + 1]

        else:  # Round end -> Remaking the turn order
            self.order = self.get_turn_order()
            self.current_monster = self.order[0]

        return

    def end_round(self) -> None:
        """End the current round."""
        self.round += 1
        return

    def end_combat(self) -> None:
        """End combat between teams of monsters."""
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
            if not monster.is_alive():
                team = self.get_team(member=monster)
                team.status = team.get_status()

                self.logger.log(
                    namespace="combat",
                    message_group="COMBAT",
                    key="death",
                    name=monster.name,
                )

                # Cleaning monster effects
                monster.effects = []

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

    def run(self) -> Dict:
        """
        Runs combat until only one team remains alive.
        """
        # Combat Start
        self.start_combat()
        self.check_deaths()
        combat_status = self.check_combat_status()

        while combat_status["status"] == "ONGOING":
            # Round Start
            self.logger.log_round(self.round)

            self.start_round()
            self.check_deaths()

            combat_status = self.check_combat_status()
            if combat_status["status"] != "ONGOING":
                break

            self.order = self.get_turn_order()
            for monster in self.order:
                # Setup
                self.current_monster = monster

                # Turn Start
                self.logger.log_turn_start(self.current_monster)
                self.logger.log_teams(self.teams)

                self.start_turn()
                self.check_deaths()

                combat_status = self.check_combat_status()
                if combat_status["status"] != "ONGOING":
                    break

                # Turn Action
                if monster.is_alive():
                    self.take_turn()
                    self.check_deaths()

                    combat_status = self.check_combat_status()
                    if combat_status["status"] != "ONGOING":
                        break

                # Turn End
                if combat_status["status"] == "ONGOING":
                    self.end_turn()
                    self.check_deaths()

                    combat_status = self.check_combat_status()
                    if combat_status["status"] != "ONGOING":
                        break

            # Round End
            if combat_status["status"] == "ONGOING":
                self.end_round()
                self.check_deaths()

                combat_status = self.check_combat_status()
                if combat_status["status"] != "ONGOING":
                    break

        self.end_combat()

        return combat_status
