"""Tests for combat team management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.manager import CombatManager


def test_get_team(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster = combat_manager.teams[0].members[0]

    team = combat_manager.get_team(member=monster)

    conditions = [
        len(team.members) == 3,
        team.members[0].local_id == "MONSTER_0",
        team.members[1].local_id == "MONSTER_1",
        team.members[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_allies(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster = combat_manager.teams[0].members[0]

    allies = combat_manager.get_allies(monster)

    conditions = [
        len(allies) == 2,
        allies[0].local_id == "MONSTER_1",
        allies[1].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_get_enemies(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster = combat_manager.teams[0].members[0]

    enemies = combat_manager.get_enemies(monster)

    conditions = [
        len(enemies) == 2,
        enemies[0].local_id == "MONSTER_3",
        enemies[1].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_team_status(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    teams_status = []

    for idx, team in enumerate(combat_manager.teams):
        for monster in team.members:
            if idx == 1:
                monster.hp = 0

        teams_status.append(team.get_status())

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "DEFEATED",
    ]

    assert_conditions(conditions)


def test_get_combat_status_winner(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for idx, team in enumerate(combat_manager.teams):
        for monster in team.members:
            if idx == 1:
                monster.hp = 0

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "WINNER",
        len(combat_status["ALIVE"]) == 1,
        len(combat_status["ALIVE"][0].members) == 3,
        len(combat_status["DEFEATED"]) == 1,
        len(combat_status["DEFEATED"][0].members) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_draw(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for team in combat_manager.teams:
        for monster in team.members:
            monster.hp = 0

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "DRAW",
        len(combat_status["ALIVE"]) == 0,
        len(combat_status["DEFEATED"]) == 2,
        len(combat_status["DEFEATED"][0].members) == 3,
        len(combat_status["DEFEATED"][1].members) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_ongoing(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "ONGOING",
        len(combat_status["ALIVE"]) == 2,
        len(combat_status["ALIVE"][0].members) == 3,
        len(combat_status["ALIVE"][1].members) == 2,
        len(combat_status["DEFEATED"]) == 0,
    ]

    assert_conditions(conditions)
