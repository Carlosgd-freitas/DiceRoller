"""Pytest configuration file for tests."""

from typing import Dict

from pytest import fixture

from src.base.monster import Monster
from src.combat.manager import CombatManager, OrderStrategy


@fixture()
def managers() -> Dict:
    monster_0 = Monster(
        local_id="MONSTER_0",
        name="Red",
        hp=0,
        max_hp=200,
        speed=0,
    )

    monster_1 = Monster(
        local_id="MONSTER_1",
        name="Green",
        hp=1,
        max_hp=200,
        speed=5,
    )

    monster_2 = Monster(
        local_id="MONSTER_2",
        name="Yellow",
        hp=10,
        max_hp=200,
        speed=1,
    )

    monster_3 = Monster(
        local_id="MONSTER_3",
        name="Blue",
        hp=100,
        max_hp=200,
        speed=10,
    )

    monster_4 = Monster(
        local_id="MONSTER_4",
        name="Purple",
        hp=200,
        max_hp=200,
        speed=1,
    )

    teams = [
        [monster_0, monster_1, monster_2],
        [monster_3, monster_4],
    ]

    team_names = [
        "Team Red",
        "Team Blue",
    ]

    combat_manager = CombatManager(
        teams=teams,
        team_names=team_names,
        order_strategy=OrderStrategy.SET,
        logging=False,
    )

    combat_manager.start_combat()

    return {
        # Variables
        "teams": teams,
        "team_names": team_names,
        # Managers
        "combat_manager": combat_manager,
        "effect_manager": combat_manager.effect_manager,
        "selector_manager": combat_manager.selector_manager,
        "suffix_manager": combat_manager.suffix_manager,
    }
