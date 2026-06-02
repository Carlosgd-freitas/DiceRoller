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
