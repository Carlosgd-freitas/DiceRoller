"""Combat Manager module."""

from random import shuffle
from src.base.side import Side
from src.base.entity import Entity
from src.base.triggers import Trigger
from typing import List, Literal, Dict
from src.combat.logger import CombatLogger
from src.processors.sides import process_side
from src.processors.targets import get_targets
from src.base.monster import Monster, ControlType


class CombatManager():
    """
    Combat Manager class.

    :var teams: Teams of characters or monsters that will fight each other.
    :vartype teams: List[List[Monster]]

    :var team_names: Teams of team names. If passed as a parameter, must have the same
    length as 'teams' parameter.
    :vartype team_names: str

    :var order_strategy: How the turn order will be decided. Default value is "FASTER".
    :vartype order_strategy: Literal["FASTER", "SET", "SHUFFLE", "SLOWER"]

    :var current_monster_id: The current monster which turn will be taken. A monster's
    local_id can be passed to be defined as the current monster. Default value is None.
    :vartype current_monster_id: str

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
        current_monster_id: str = None,
    ):
        self.round: int = 0
        self.turn: int = 0

        self.logger: CombatLogger = CombatLogger()
        teams = [] if teams is None else list(teams)
        team_names = [] if team_names is None else list(team_names)

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
        # Reminder + ToDo: Dead monsters are not deleted from order, their actions just don't
        # take place.

        self.current_monster_id = current_monster_id
        self.current_monster = self.get_monster(self.current_monster_id)

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
            order.sort(key = lambda x: x.speed, reverse=True)

        elif self.order_strategy == "SLOWER":
            order.sort(key = lambda x: x.speed)

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
            if (type == "SELF") \
                and (team[0].team_name == monster.team_name):
                    return [
                        team_monster for team_monster in team
                    ]

            elif (type == "ALLIES") \
                and (team[0].team_name == monster.team_name):
                return [
                    team_monster for team_monster in team
                    if team_monster.local_id != monster.local_id
                ]

            elif (type == "ENEMIES") \
                and (team[0].team_name != monster.team_name):
                    selected.extend([
                        team_monster for team_monster in team
                    ])

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

    def get_combat_result(self) -> Dict:
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

        if (len(teams_status["ALIVE"]) == 0):
            teams_status["status"] = "DRAW"

        elif (len(teams_status["ALIVE"]) == 1):
            teams_status["status"] = "WINNER"

        else:
            teams_status["status"] = "ONGOING"

        return teams_status

    def roll(self, entity: Entity) -> List[Side]:
        """Roll an Entity's dice and returns the rolled Sides."""
        rolled = []

        rolling_effects = [
            effect
            for effect in entity.effects
            if effect.trigger == Trigger.ROLL
        ]

        for dice in entity.dice:
            rolled.append(dice.roll())

            for effect in rolling_effects:
                effect.activate(
                    None,
                    entity,
                )

        return rolled

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
        self.current_monster_id = self.order[0].local_id
        self.current_monster = self.get_monster(self.current_monster_id)
        return

    def start_round(self) -> None:
        """Start the current round."""
        self.round += 1
        self.turn = 0
        return

    def start_turn(self) -> None:
        """Start the current monster's turn."""
        self.turn += 1

        for effect in self.current_monster.effects:
            if effect.trigger == Trigger.TURN_START:
                effect.activate(
                    None,
                    self.current_monster,
                )

        return

    def take_turn(self) -> None:
        """The current monster takes its turn."""
        if self.current_monster.control_type == ControlType.AI:
            sides = self.current_monster.roll()
            current_team = self.get_team(self.current_monster)
            enemies = self.get_team(self.current_monster, "ENEMIES")

            for side in sides:
                targets = get_targets(
                    current_monster=self.current_monster,
                    side=side,
                    current_team=current_team,
                    enemies=enemies,
                )
                targets = process_side(
                    side=side,
                    source=self.current_monster,
                    targets=targets,
                )

        elif self.current_monster.control_type == ControlType.PLAYER:
            raise NotImplementedError()

        return

    def end_turn(self) -> Dict:
        """
        End the current monster's turn. All effects on the current monsters will be
        decayed and removed if their duration are <= 0.

        :return: A dictionary containing objects that were affected by the turn ending.
        :rtype: Dict

        **Return keys**
        * ``removed_effects``: a list of effects that were removed from the current
        monster
        """
        # Procesing effects on turn end
        for effect in self.current_monster.effects:
            if effect.trigger == Trigger.TURN_END:
                effect.activate(
                    None,
                    self.current_monster,
                )

        # Decaying and removing effects
        idx_removed_effects = []

        for idx, effect in enumerate(self.current_monster.effects):
            effect.duration -= 1
            effect.value -= effect.decay

            if effect.duration <= 0:
                idx_removed_effects.append(idx)

        removed_effects = [
            effect for idx, effect in enumerate(self.current_monster.effects)
            if idx in idx_removed_effects
        ]
        self.current_monster.effects = [
            effect for idx, effect in enumerate(self.current_monster.effects)
            if idx not in idx_removed_effects
        ]

        return {
            "removed_effects": removed_effects,
        }

    def next_turn(self) -> None:
        """Sets up next monster turn."""

        idx_monster: int = None
        for idx, monster in enumerate(self.order):
            if monster.local_id == self.current_monster_id:
                idx_monster = idx
                break

        while True:
            idx_monster += 1

            monster = self.order[idx_monster % len(self.order)]

            if monster.hp > 0:
                self.current_monster_id = monster.local_id
                self.current_monster = self.get_monster(self.current_monster_id)
                break

        return

    def end_round(self) -> None:
        """End the current round."""
        return

    def end_combat(self) -> None:
        """End combat between teams of monsters."""
        return
