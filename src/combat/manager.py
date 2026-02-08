"""Combat Manager module."""

from random import shuffle
from typing import List, Literal, Dict
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
        teams: List[List[Monster]] = [],
        team_names: List[str] = [],
        order_strategy: Literal["FASTER", "SET", "SHUFFLE", "SLOWER"] = "FASTER",
        current_monster_id: Monster | str = None,
    ):
        self.turn: int = 1

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

        self.teams: List[List[Monster]] = teams

        self.order_strategy = order_strategy
        self.order = self._set_order()
        # Reminder: Dead monsters are not deleted from order, their actions just don't
        # take place.

        self.current_monster_id = current_monster_id

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
        for monster in self.order:
            if monster.local_id == monster_local_id:
                return monster
        return None
    
    def get_team(
        self,
        type: Literal["ALLIES", "ENEMIES"] = None,
        current_monster: Monster = None,
        team_name: str = None,
    ) -> List[Monster]:
        """
        Get a team (list) of monsters.

        :param type: A type of team. Default value is None.
        :type type: Literal["ALLIES", "ENEMIES"]

        :param current_monster: The current Monster. This parameter must be passed if
        type is passed.
        :type current_monster: Monster

        :param team_name: A monster team's name.
        :type team_name: str

        **Team types**
        * ``ALLIES``: all other monsters from the same team
        * ``ENEMIES``: all monsters from different teams

        :return: A list of monsters from the same team.
        :rtype: List[Monster]
        """

        if type == "ALLIES":
            return [
                monster for monster in self.order
                if (
                    (monster.team == current_monster.team)
                    and (monster.local_id != current_monster.local_id)
                )
            ]

        elif type == "ENEMIES":
            return [
                monster for monster in self.order
                if monster.team != current_monster.team
            ]
        
        elif team_name:
            return [
                monster for monster in self.order
                if monster.team == team_name
            ]

        return []

    # ToDo: Testing
    def get_team_status(
        self,
        team: List[Monster]
    ) -> Literal["ALIVE", "DEFEATED"]:
        """
        Returns the status of liveness of a list of monsters:
        * ``ALIVE``: if at least one monster has their hp > 0
        * ``DEFEATED``: if all monsters have their hp = 0

        :param team: A list of monsters.
        :type team: List[Monster]

        :return: Team status.
        :rtype: Literal["ALIVE", "DEFEATED"]
        """
        status: str = "DEFEATED"

        for monster in team:
            if monster.hp > 0:
                status = "ALIVE"
                break

        return status

    # ToDo: Testing
    def get_result(self) -> Dict:
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
            team_status = self.get_team_status(team)
            teams_status[team_status].append(team)

        if (len(teams_status["ALIVE"]) == 0):
            teams_status["status"] = "DRAW"

        elif (len(teams_status["ALIVE"]) == 1):
            teams_status["status"] = "WINNER"

        else:
            teams_status["status"] = "ONGOING"

        return teams_status

    def start_combat(self) -> None:
        """Start combat between teams of monsters."""
        self.current_monster_id = self.order[0].local_id
        return

    def take_turn(self) -> None:
        """The current monster takes its turn."""
        current_monster = self.get_monster(self.current_monster_id)

        # Turn start

        # Take actions
        if current_monster.control_type == ControlType.AI:
            sides = current_monster.roll()
            allies = self.get_team(type="ALLIES", current_monster=current_monster)
            enemies = self.get_team(type="ENEMIES", current_monster=current_monster)

            for side in sides:
                targets = get_targets(current_monster, side, allies, enemies)
                targets = process_side(side, targets)

        elif current_monster.control_type == ControlType.PLAYER:
            raise NotImplementedError()

        # Turn end
        return

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
                break

        return

    def end_combat(self) -> None:
        """End combat between teams of monsters."""
        return
