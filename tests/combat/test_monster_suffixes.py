"""Tests for monster suffixes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.monster import Monster
from src.combat.team import Team
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.manager import CombatManager, SuffixManager


def test_increase_suffix(managers: Dict):
    suffix_manager: SuffixManager = managers["suffix_manager"]

    conditions = [
        suffix_manager.increase_suffix("A") == "B",
        suffix_manager.increase_suffix("B") == "C",
        suffix_manager.increase_suffix("Z") == "AA",
        suffix_manager.increase_suffix("AA") == "AB",
        suffix_manager.increase_suffix("AB") == "AC",
        suffix_manager.increase_suffix("AZ") == "BA",
        suffix_manager.increase_suffix("BA") == "BB",
        suffix_manager.increase_suffix("BB") == "BC",
        suffix_manager.increase_suffix("BZ") == "CA",
        suffix_manager.increase_suffix("ZA") == "ZB",
        suffix_manager.increase_suffix("ZB") == "ZC",
        suffix_manager.increase_suffix("ZZ") == "AAA",
    ]

    assert_conditions(conditions)


def test_monster_suffixes_none(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    conditions = [
        combat_manager.teams[0].members[0].suffix is None,
        combat_manager.teams[0].members[1].suffix is None,
        combat_manager.teams[0].members[2].suffix is None,
        combat_manager.teams[1].members[0].suffix is None,
        combat_manager.teams[1].members[1].suffix is None,
    ]

    assert_conditions(conditions)


def test_monster_suffixes_simple(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    suffix_manager: SuffixManager = managers["suffix_manager"]

    team_0 = Team(
        members=[
            Monster(name="Red"),
            Monster(name="Red"),
            Monster(name="Red"),
        ]
    )

    team_1 = Team(
        members=[
            Monster(name="Blue"),
            Monster(name="Blue"),
        ]
    )

    combat_manager.teams = [team_0, team_1]

    suffix_manager.add_suffixes(combat_manager.teams)

    conditions = [
        combat_manager.teams[0].members[0].suffix == "A",
        combat_manager.teams[0].members[1].suffix == "B",
        combat_manager.teams[0].members[2].suffix == "C",
        combat_manager.teams[1].members[0].suffix == "A",
        combat_manager.teams[1].members[1].suffix == "B",
    ]

    assert_conditions(conditions)


def test_monster_suffixes_add_monster(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    monster = Monster(
        local_id="MONSTER_5",
        name="Red",
    )

    conditions = [
        combat_manager.teams[0].members[0].suffix is None,
        combat_manager.teams[0].members[1].suffix is None,
        combat_manager.teams[0].members[2].suffix is None,
        combat_manager.teams[1].members[0].suffix is None,
        combat_manager.teams[1].members[1].suffix is None,
    ]

    combat_manager.add_monster(monster=monster, team_name="Team Blue")

    conditions.extend(
        [
            combat_manager.teams[0].members[0].suffix == "A",
            combat_manager.teams[0].members[1].suffix is None,
            combat_manager.teams[0].members[2].suffix is None,
            combat_manager.teams[1].members[0].suffix is None,
            combat_manager.teams[1].members[1].suffix is None,
            combat_manager.teams[1].members[2].suffix == "B",
        ]
    )

    assert_conditions(conditions)


def test_monster_suffixes_remove_monster(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.remove_monster(
        monster=combat_manager.teams[0].members[0],
    )

    monster = Monster(
        local_id="MONSTER_5",
        name="Red",
    )

    combat_manager.add_monster(monster=monster, team_name="Team Blue")

    conditions = [
        combat_manager.teams[0].members[0].suffix is None,
        combat_manager.teams[0].members[1].suffix is None,
        combat_manager.teams[1].members[0].suffix is None,
        combat_manager.teams[1].members[1].suffix is None,
        combat_manager.teams[1].members[2].suffix is None,
    ]

    assert_conditions(conditions)
