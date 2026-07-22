"""Tests for Team class."""

from copy import deepcopy
from typing import Dict, List

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.base.team import Team
from src.effects.attack import AttackEffect
from tests.utils import assert_conditions


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


def test_team_is_equivalent():
    effect = AttackEffect(Stat(flat=1))
    side = Side(effects=[effect])
    dice = Dice(sides=[side])

    monster_0 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[dice],
    )

    monster_1 = Monster(
        global_id="ID_1",
        hp=1,
        max_hp=2,
        dice=[dice],
    )

    team_0 = Team(
        members=[deepcopy(monster_0)],
    )

    team_1 = Team(
        members=[deepcopy(monster_0)],
    )

    team_2 = Team(
        members=[deepcopy(monster_1)],
    )

    conditions = [
        team_0.is_equivalent(team_0) is True,
        team_0.is_equivalent(team_1) is True,
        team_0.is_equivalent(team_2) is False,
    ]

    assert_conditions(conditions)
