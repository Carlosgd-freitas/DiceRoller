"""Team module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal

if TYPE_CHECKING:
    from src.base.monster import Monster


class Team:
    """
    Team class.

    :var name: Team's name.
    :vartype name: str

    :var members: Team's members.
    :vartype members: List[Monster]

    :var status: Team's status.
    :vartype status: Literal["ALIVE", "DEFEATED"]
    """

    def __init__(
        self,
        name: str = None,
        members: List[Monster] = None,
    ):
        self.name = name
        self.members = [] if members is None else members
        self.status = self.get_status()

    def __str__(self) -> str:
        """String representation of Team."""
        _str = f"{self.name}"

        _str += f"\n>>>>> Members ({len(self.members)}):"
        for member in self.members:
            _str += f"\n>>>> {member}\n"

        return _str

    def get_status(self) -> Literal["ALIVE", "DEFEATED"]:
        """
        Returns the liveness status of the team:
        * ``ALIVE``: if at least one member is alive
        * ``DEFEATED``: if all members are dead

        :return: Team status.
        :rtype: Literal["ALIVE", "DEFEATED"]
        """
        status = "DEFEATED"

        for member in self.members:
            if member.is_alive():
                status = "ALIVE"
                break

        return status

    def is_equivalent(self, team: Team) -> bool:
        """
        Compares two teams and returns if they are equivalent.

        :param team: Team for comparison.
        :type team: Team

        :return: If the teams are equivalent.
        :rtype: bool
        """
        return (
            isinstance(team, Team)
            and len(self.members) == len(team.members)
            and all(
                [
                    self_member.is_equivalent(member)
                    for self_member, member in zip(
                        self.members, team.members, strict=True
                    )
                ]
            )
        )

    def is_member(self, monster: Monster) -> bool:
        """
        Returns if a monster is a member of the team or not.

        :return: If the monster is a member of the team or not.
        :rtype: bool
        """
        for member in self.members:
            if member == monster:
                return True

        return False
