"""Tests for Team class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.team import Team


def test_get_team_status(combat: Dict):
    teams: List[Team] = combat["teams"]
    teams_status = []

    for idx, team in enumerate(teams):
        for monster in team.members:
            if idx == 1:
                monster.hp = 0

        teams_status.append(team.get_status())

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "DEFEATED",
    ]

    assert_conditions(conditions)
