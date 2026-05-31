"""Tests for monster suffixes."""

from typing import Dict

from src.base.monster import Monster
from src.combat.manager import CombatManager
from tests.utils import assert_conditions


def test_increase_suffix(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    conditions = [
        combat_manager.increase_suffix("A") == "B",
        combat_manager.increase_suffix("B") == "C",
        combat_manager.increase_suffix("Z") == "AA",
        combat_manager.increase_suffix("AA") == "AB",
        combat_manager.increase_suffix("AB") == "AC",
        combat_manager.increase_suffix("AZ") == "BA",
        combat_manager.increase_suffix("BA") == "BB",
        combat_manager.increase_suffix("BB") == "BC",
        combat_manager.increase_suffix("BZ") == "CA",
        combat_manager.increase_suffix("ZA") == "ZB",
        combat_manager.increase_suffix("ZB") == "ZC",
        combat_manager.increase_suffix("ZZ") == "AAA",
    ]

    assert_conditions(conditions)


def test_monster_suffixes_none(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    conditions = [
        combat_manager.teams[0][0].suffix is None,
        combat_manager.teams[0][1].suffix is None,
        combat_manager.teams[0][2].suffix is None,
        combat_manager.teams[1][0].suffix is None,
        combat_manager.teams[1][1].suffix is None,
    ]

    assert_conditions(conditions)


def test_monster_suffixes_simple(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    team_0 = [
        Monster(name="Red"),
        Monster(name="Red"),
        Monster(name="Red"),
    ]

    team_1 = [
        Monster(name="Blue"),
        Monster(name="Blue"),
    ]

    combat_manager.teams = [team_0, team_1]

    combat_manager.add_suffixes()

    conditions = [
        combat_manager.teams[0][0].suffix == "A",
        combat_manager.teams[0][1].suffix == "B",
        combat_manager.teams[0][2].suffix == "C",
        combat_manager.teams[1][0].suffix == "A",
        combat_manager.teams[1][1].suffix == "B",
    ]

    assert_conditions(conditions)


def test_monster_suffixes_add_monster(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    monster = Monster(
        local_id="MONSTER_5",
        name="Red",
    )

    conditions = [
        combat_manager.teams[0][0].suffix is None,
        combat_manager.teams[0][1].suffix is None,
        combat_manager.teams[0][2].suffix is None,
        combat_manager.teams[1][0].suffix is None,
        combat_manager.teams[1][1].suffix is None,
    ]

    combat_manager.add_monster(monster=monster, team_name="Team Blue")

    conditions.extend(
        [
            combat_manager.teams[0][0].suffix == "A",
            combat_manager.teams[0][1].suffix is None,
            combat_manager.teams[0][2].suffix is None,
            combat_manager.teams[1][0].suffix is None,
            combat_manager.teams[1][1].suffix is None,
            combat_manager.teams[1][2].suffix == "B",
        ]
    )

    assert_conditions(conditions)


def test_monster_suffixes_remove_monster(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.remove_monster(
        monster=combat_manager.teams[0][0],
    )

    monster = Monster(
        local_id="MONSTER_5",
        name="Red",
    )

    combat_manager.add_monster(monster=monster, team_name="Team Blue")

    conditions = [
        combat_manager.teams[0][0].suffix is None,
        combat_manager.teams[0][1].suffix is None,
        combat_manager.teams[1][0].suffix is None,
        combat_manager.teams[1][1].suffix is None,
        combat_manager.teams[1][2].suffix is None,
    ]

    assert_conditions(conditions)
