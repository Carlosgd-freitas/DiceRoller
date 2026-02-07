"""Combat Manager module."""

from random import shuffle
from typing import List, Literal
from processors.side import process_side
from processors.target import get_targets
from base.monster import Monster, ControlType


class CombatManager():
    """
    Combat Manager class.

    :var teams: Teams of characters or monsters that will fight eachother.
    :vartype teams: List[Monster]

    :var current_monster_id: The current monster which turn will be taken. A monster's
    local_id can be passed to be defined as the current monster. Default value is None.
    :vartype current_monster_id: str
    """

    def __init__(
        self,
        teams: List[List[Monster]] = [],
        current_monster_id: Monster | str = None,
    ):
        self.turn: int = 1

        for idx, team in enumerate(teams):
            default_team_name = f"TEAM_{idx}"

            for monster in team:
                if monster.team is None:
                    monster.team = default_team_name
        self.teams: List[Monster] = teams

        self.order = self._set_order()
        # Reminder: Dead monsters are not deleted from order, their actions just don't
        # take place.

        self.current_monster_id = current_monster_id

    def _set_order(
        self,
        strategy: Literal["SET", "SHUFFLE", "SPEED"] = "SPEED",
    ) -> List[Monster]:
        """
        Returns the order in which characters and monsters will take action.

        :return: A list of monsters.
        :rtype: List[Monster]
        """
        order: List[Monster] = [monster for team in self.teams for monster in team]

        if strategy == "SHUFFLE":
            shuffle(order)
        
        elif strategy == "SPEED":
            order.sort(key = lambda x: x.speed)

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

        :param type: A type of team. If equal to "ALLIES", all other monsters from the same team will be returned.
        If equal to "ENEMIES", all monsters from different teams will be returned. Default value is None.
        :type type: Literal["ALLIES", "ENEMIES"]

        :param current_monster: The current Monster. This parameter must be passed if
        type is passed.
        :type current_monster: Monster

        :param team_name: A monster team's name.
        :type team_name: str

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

    def take_turn(self):
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
