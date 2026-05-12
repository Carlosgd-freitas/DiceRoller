"""Pytest configuration file for processing tests."""

from typing import Dict
from pytest import fixture
from src.base.monster import Monster
from src.combat.manager import CombatManager


@fixture
def effect_processing() -> Dict:
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=5,
        max_hp=10,
        mana=0,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=5,
        max_hp=10,
        mana=0,
    )

    combat_manager = CombatManager(
        teams=[
            [monster_0],
            [monster_1],
        ],
        order_strategy="SET",
    )

    combat_manager.start_combat()

    return {
        "combat_manager": combat_manager
    }
