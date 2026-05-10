"""Tests for combat team management."""

from pytest import fixture
from src.base.monster import Monster
from src.combat.manager import CombatManager


@fixture
def combat_manager():
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=10,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=0,
    )
    monster_2 = Monster(
        local_id="MONSTER_2",
        hp=0,
    )

    teams = [
        [monster_0, monster_1],
        [monster_2]
    ]

    combat_manager = CombatManager(
        teams=teams,
        order_strategy="SET",
    )

    return combat_manager


def test_get_team_self(combat_manager: CombatManager):
    monster_local_ids = []

    for monster in combat_manager.order:
        team = combat_manager.get_team(monster)

        for team_monster in team:
            monster_local_ids.append(team_monster.local_id)

    conditions = [
        len(monster_local_ids) == 5,

        monster_local_ids[0] == "MONSTER_0",
        monster_local_ids[1] == "MONSTER_1",

        monster_local_ids[2] == "MONSTER_0",
        monster_local_ids[3] == "MONSTER_1",

        monster_local_ids[4] == "MONSTER_2",
    ]

    assert all(conditions)


def test_get_team_allies(combat_manager: CombatManager):
    monster_local_ids = []

    for monster in combat_manager.order:
        team = combat_manager.get_team(monster, "ALLIES")

        for team_monster in team:
            monster_local_ids.append(team_monster.local_id)

    conditions = [
        len(monster_local_ids) == 2,

        monster_local_ids[0] == "MONSTER_1",

        monster_local_ids[1] == "MONSTER_0",
    ]

    assert all(conditions)


def test_get_team_enemies(combat_manager: CombatManager):
    monster_local_ids = []

    for monster in combat_manager.order:
        team = combat_manager.get_team(monster, "ENEMIES")

        for team_monster in team:
            monster_local_ids.append(team_monster.local_id)

    conditions = [
        len(monster_local_ids) == 4,

        monster_local_ids[0] == "MONSTER_2",

        monster_local_ids[1] == "MONSTER_2",

        monster_local_ids[2] == "MONSTER_0",
        monster_local_ids[3] == "MONSTER_1",
    ]

    assert all(conditions)


def test_get_team_status_monster(combat_manager: CombatManager):
    teams_status = []

    for monster in combat_manager.order:
        teams_status.append(
            combat_manager.get_team_status(monster=monster)
        )

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "ALIVE",
        teams_status[2] == "DEFEATED",
    ]

    assert all(conditions)


def test_get_team_status_team(combat_manager: CombatManager):
    teams_status = []

    for team in combat_manager.teams:
        teams_status.append(
            combat_manager.get_team_status(team=team)
        )

    conditions = [
        teams_status[0] == "ALIVE",
        teams_status[1] == "DEFEATED",
    ]

    assert all(conditions)


def test_get_combat_result_winner(combat_manager: CombatManager):
    result = combat_manager.get_combat_result()

    conditions = [
        result["status"] == "WINNER",

        len(result["ALIVE"]) == 1,
        len(result["ALIVE"][0]) == 2,

        len(result["DEFEATED"]) == 1,
        len(result["DEFEATED"][0]) == 1,
    ]

    assert all(conditions)


def test_get_combat_result_draw(combat_manager: CombatManager):
    combat_manager.order[0].hp = 0

    result = combat_manager.get_combat_result()

    conditions = [
        result["status"] == "DRAW",

        len(result["ALIVE"]) == 0,

        len(result["DEFEATED"]) == 2,
        len(result["DEFEATED"][0]) == 2,
        len(result["DEFEATED"][1]) == 1,
    ]

    assert all(conditions)


def test_get_combat_result_ongoing(combat_manager: CombatManager):
    combat_manager.order[2].hp = 10

    result = combat_manager.get_combat_result()

    conditions = [
        result["status"] == "ONGOING",

        len(result["ALIVE"]) == 2,
        len(result["ALIVE"][0]) == 2,
        len(result["ALIVE"][1]) == 1,

        len(result["DEFEATED"]) == 0,
    ]

    assert all(conditions)
