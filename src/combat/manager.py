"""Combat Manager module."""

from random import random, shuffle
from typing import Dict, List, Literal, TypedDict

from src.base.effect import Effect, EffectType
from src.base.entity import Entity
from src.base.keywords import Keyword
from src.base.monster import ControlType, Monster
from src.base.side import Side
from src.base.triggers import Trigger
from src.logger.logger import Logger
from src.targeting.selectors.manager import SelectorManager


class CombatResult(TypedDict):
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

    :var order_strategy: How the turn order will be decided. Default value is "FASTER".
    :vartype order_strategy: Literal["FASTER", "SET", "SHUFFLE", "SLOWER"]

    :var logging: If the combat will be logged. Default value is True.
    :vartype logging: bool

    :var language: What language will be logged. Default value is "EN-US".
    :vartype language: Literal["EN-US", "PT-BR"]

    **Order strategies**
    * ``FASTER``: monsters act from highest to lowest speed
    * ``SET``: monsters act in the order they are provided
    * ``SHUFFLE``: monsters act in random order
    * ``SLOWER``: monsters act from lowest to highest speed
    """

    def __init__(
        self,
        teams: List[List[Monster]] = None,
        team_names: List[str] = None,
        order_strategy: Literal["FASTER", "SET", "SHUFFLE", "SLOWER"] = "FASTER",
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
        self.order = self._set_order()

    def _set_order(
        self,
    ) -> List[Monster]:
        """
        Returns the order in which characters and monsters will take action.

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        order: List[Monster] = [monster for team in self.teams for monster in team]

        if self.order_strategy == "FASTER":
            order.sort(key=lambda x: x.speed, reverse=True)

        elif self.order_strategy == "SLOWER":
            order.sort(key=lambda x: x.speed)

        elif self.order_strategy == "SHUFFLE":
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
            if team_monster.hp > 0:
                status = "ALIVE"
                break

        return status

    def get_combat_result(self) -> CombatResult:
        """
        Returns the current result of the combat.

        :return: Team status
        :rtype: Dict

        **Return keys**
        * ``ALIVE``: a list of teams (list of monsters) with at least one monster with
        hp > 0
        * ``DEFEATED``: a list of teams (list of monsters) with all monsters with
        hp = 0
        * ``status``: current combat result:
          * "DRAW": the combat only has defeated teams
          * "ONGOING": the combat may still continue
          * "WINNER": the combat has only one alive team
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
        monster.team_name = team_name

        for team in self.teams:
            if team[0].team_name == team_name:
                team.append(monster)
                break
        else:
            self.teams.append([monster])

        self.order = self._set_order()

        return

    def remove_monster(
        self,
        monster: Monster,
    ) -> None:
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
        for monster in self.order[:]:
            if monster.hp <= 0:
                self.logger.log(key="death", name=monster.name)
                self.remove_monster(monster)

        return

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

        # Logging effects
        if effect_data is None:
            effect_data = {}

        key = effect.keyword.value.lower()

        if source == target:
            key += "_self"

        self.logger.log(
            key=key,
            source=source.name,
            target=target.name,
            value=effect.value,
            damage=effect_data.get("damage"),
        )

        # Procesing effects on being attacked
        if effect.type == EffectType.OFFENSIVE:
            for target_effect in target.effects:
                if target_effect.trigger == Trigger.BEING_ATTACKED:
                    target_effect.activate(
                        source=target,
                        target=source,
                    )

        return True

    def roll(self, entity: Entity) -> List[Side]:
        """
        Rolls all Entity's dice and returns the rolled Sides. The entity will be
        affected by Effects that triggers on dice roll.

        :param entity: An Entity.
        :type entity: Entity
        """
        rolled = []

        rolling_effects = [
            effect for effect in entity.effects if effect.trigger == Trigger.ROLL
        ]

        for dice in entity.dice:
            rolled.append(dice.roll())

            for effect in rolling_effects:
                effect.activate(
                    target=entity,
                )

        return rolled

    def process_trigger(
        self,
        trigger: Trigger,
        target: Monster,
        source: Monster | None = None,
    ) -> None:
        if not target:
            return

        for effect in target.effects[:]:
            if effect.trigger == trigger:
                effect.activate(
                    target=target,
                    source=source,
                )

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
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
        source: Monster,
    ) -> None:
        sides = self.roll(source)

        allies = self.get_team(source, "ALLIES")
        enemies = self.get_team(source, "ENEMIES")

        for side in sides:
            targets = self.selector_manager.get_targets(
                side=side,
                source=source,
                allies=allies,
                enemies=enemies,
                k=1,
                difficulty=source.difficulty,
            )

            for target in targets:
                for effect in side.effects:
                    self.execute_effect(
                        effect=effect,
                        source=source,
                        target=target,
                    )

    def take_turn(self) -> None:
        if self.current_monster.control_type == ControlType.AI:
            self.take_action(self.current_monster)

        elif self.current_monster.control_type == ControlType.PLAYER:
            raise NotImplementedError

        return

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

        while self.get_combat_result()["status"] == "ONGOING":
            self.start_round()
            self.check_deaths()

            self.logger.log_round(self.round)
            self.logger.log_teams(self.teams)

            for monster in self.order:
                self.current_monster = monster

                self.start_turn()
                self.check_deaths()

                if monster.hp > 0:
                    self.logger.log(key="turn", name=self.current_monster.name)
                    self.take_turn()
                    self.check_deaths()

                self.end_turn()
                self.check_deaths()

                combat_result = self.get_combat_result()
                if combat_result["status"] == "DRAW":
                    self.logger.log(key="draw")
                    break

                elif combat_result["status"] == "WINNER":
                    self.logger.log(
                        key="winner", team_name=combat_result["ALIVE"][0][0].team_name
                    )
                    break

            self.end_round()
            self.check_deaths()

        self.end_combat()

        return self.get_combat_result()
