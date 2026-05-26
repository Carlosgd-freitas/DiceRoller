"""Pytest configuration file for tests."""

from typing import Dict

from pytest import fixture

from src.base.monster import Monster
from src.combat.manager import CombatManager
from src.targeting.selectors.manager import SelectorManager


@fixture()
def managers() -> Dict:
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=0,
        max_hp=200,
    )

    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=1,
        max_hp=200,
    )

    monster_2 = Monster(
        local_id="MONSTER_2",
        hp=10,
        max_hp=200,
    )

    monster_3 = Monster(
        local_id="MONSTER_3",
        hp=100,
        max_hp=200,
    )

    monster_4 = Monster(
        local_id="MONSTER_4",
        hp=200,
        max_hp=200,
    )

    combat_manager = CombatManager(
        teams=[
            [monster_0, monster_1, monster_2],
            [monster_3, monster_4],
        ],
        order_strategy="SET",
        logging=False,
    )

    combat_manager.start_combat()

    selector_manager = SelectorManager()

    return {
        "combat_manager": combat_manager,
        "selector_manager": selector_manager,
    }
