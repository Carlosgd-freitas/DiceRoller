"""Tests for TeamManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.team import Team
    from src.combat.team_manager import TeamManager


def test_get_team(combat: Dict):
    team_manager: TeamManager = combat["team_manager"]
    teams: List[Team] = combat["teams"]
    monster = teams[0].members[0]

    team = team_manager.get_team(member=monster, teams=teams)

    conditions = [
        len(team.members) == 3,
        team.members[0].local_id == "MONSTER_0",
        team.members[1].local_id == "MONSTER_1",
        team.members[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_allies(combat: Dict):
    team_manager: TeamManager = combat["team_manager"]
    teams: List[Team] = combat["teams"]
    monster = teams[0].members[0]

    allies = team_manager.get_allies(monster, teams)

    conditions = [
        len(allies) == 2,
        allies[0].local_id == "MONSTER_1",
        allies[1].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_enemies(combat: Dict):
    team_manager: TeamManager = combat["team_manager"]
    teams: List[Team] = combat["teams"]
    monster = teams[0].members[0]

    enemies = team_manager.get_enemies(monster, teams)

    conditions = [
        len(enemies) == 2,
        enemies[0].local_id == "MONSTER_3",
        enemies[1].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)
