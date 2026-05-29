"""Tests for combat team management."""

from typing import Dict

from src.combat.manager import CombatManager
from tests.utils import assert_conditions


def test_get_team_self(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    team = combat_manager.get_team(combat_manager.teams[0][0])

    conditions = [
        len(team) == 3,
        team[0].local_id == "MONSTER_0",
        team[1].local_id == "MONSTER_1",
        team[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_team_allies(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    team = combat_manager.get_team(combat_manager.teams[0][0], "ALLIES")

    conditions = [
        len(team) == 2,
        team[0].local_id == "MONSTER_1",
        team[1].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_team_enemies(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    team = combat_manager.get_team(combat_manager.teams[0][0], "ENEMIES")

    conditions = [
        len(team) == 2,
        team[0].local_id == "MONSTER_3",
        team[1].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_team_status_monster(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    teams_status = []

    for idx, team in enumerate(combat_manager.teams):
        for monster in team:
            if idx == 1:
                monster.hp = 0

    for team in combat_manager.teams:
        for monster in team:
            teams_status.append(combat_manager.get_team_status(monster=monster))

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "ALIVE",
        teams_status[2] == "ALIVE",
        teams_status[3] == "DEFEATED",
        teams_status[4] == "DEFEATED",
    ]

    assert_conditions(conditions)


def test_get_team_status_team(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    teams_status = []

    for idx, team in enumerate(combat_manager.teams):
        for monster in team:
            if idx == 1:
                monster.hp = 0

        teams_status.append(combat_manager.get_team_status(team=team))

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "DEFEATED",
    ]

    assert_conditions(conditions)


def test_get_combat_status_winner(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    for idx, team in enumerate(combat_manager.teams):
        for monster in team:
            if idx == 1:
                monster.hp = 0

    result = combat_manager.get_combat_status()

    conditions = [
        result["status"] == "WINNER",
        len(result["ALIVE"]) == 1,
        len(result["ALIVE"][0]) == 3,
        len(result["DEFEATED"]) == 1,
        len(result["DEFEATED"][0]) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_draw(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    for team in combat_manager.teams:
        for monster in team:
            monster.hp = 0

    result = combat_manager.get_combat_status()

    conditions = [
        result["status"] == "DRAW",
        len(result["ALIVE"]) == 0,
        len(result["DEFEATED"]) == 2,
        len(result["DEFEATED"][0]) == 3,
        len(result["DEFEATED"][1]) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_ongoing(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    result = combat_manager.get_combat_status()

    conditions = [
        result["status"] == "ONGOING",
        len(result["ALIVE"]) == 2,
        len(result["ALIVE"][0]) == 3,
        len(result["ALIVE"][1]) == 2,
        len(result["DEFEATED"]) == 0,
    ]

    assert_conditions(conditions)
