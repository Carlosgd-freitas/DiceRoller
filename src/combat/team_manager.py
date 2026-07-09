"""Team Manager module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.monster import Monster

if TYPE_CHECKING:
    from src.combat.team import Team


class TeamManager:
    """
    TeamManager class.
    """

    def get_team(
        self,
        teams: List[Team],
        member: Monster = None,
        name: str = None,
    ) -> Team:
        """
        Returns a team.

        :param teams: A list of teams.
        :type teams: List[Team]

        :param member: A member of the team.
        :type member: Monster

        :param name: The name of the team.
        :type name: str

        :return: A team.
        :rtype: Team
        """
        for team in teams:
            if (name) and (team.name == name):
                return team

            elif (member) and (member in team.members):
                return team

        return

    def get_allies(
        self,
        monster: Monster,
        teams: List[Team],
    ) -> List[Monster]:
        """
        Returns all allies of a monster.

        :param monster: A monster.
        :type monster: Monster

        :param teams: A list of teams.
        :type teams: List[Team]

        :return: A list of monster allies.
        :rtype: List[Monster]
        """
        team = self.get_team(member=monster, teams=teams)

        return [
            team_monster for team_monster in team.members if team_monster != monster
        ]

    def get_enemies(
        self,
        monster: Monster,
        teams: List[Team],
    ) -> List[Monster]:
        """
        Returns all enemies of a monster.

        :param monster: A monster.
        :type monster: Monster

        :param teams: A list of teams.
        :type teams: List[Team]

        :return: A list of monster enemies.
        :rtype: List[Monster]
        """
        enemies = []
        monster_team = self.get_team(member=monster, teams=teams)

        for team in teams:
            if team != monster_team:
                enemies.extend(team.members)

        return enemies

    def add_monster(
        self,
        monster: Monster,
        teams: List[Team],
        team: Team,
    ) -> None:
        """
        Adds a monster to a team.

        :param monster: The monster which will be added.
        :type monster: Monster

        :param team: The team that the monster will be added to.
        :type team: Team
        """
        for teams_team in teams:
            if (team) and (teams_team == team):
                teams_team.members.append(monster)
                teams_team.status = teams_team.get_status()

        return

    def remove_monster(
        self,
        monster: Monster,
        teams: List[Team],
    ) -> None:
        """
        Removes a monster from a team.

        :param monster: The monster which will be removed.
        :type monster: Monster

        :param teams: A list of teams.
        :type teams: List[Team]
        """
        for team in teams:
            if monster in team.members:
                team.members.remove(monster)
                team.status = team.get_status()

        return
