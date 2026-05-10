"""Tests for combat turn management."""

from pytest import fixture
from src.base.monster import Monster
from src.combat.manager import CombatManager


@fixture
def combat_manager():
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=10,
        speed=5,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=0,
        speed=1,
    )
    monster_2 = Monster(
        local_id="MONSTER_2",
        hp=10,
        speed=10,
    )

    teams = [
        [monster_0, monster_1],
        [monster_2]
    ]

    combat_manager = CombatManager(
        teams=teams,
        order_strategy="FASTER",
    )

    combat_manager.start_combat()

    return combat_manager


def test_next_turn(combat_manager: CombatManager):
    turn_0_monster_id = combat_manager.current_monster_id

    combat_manager.next_turn()
    turn_1_monster_id = combat_manager.current_monster_id

    combat_manager.next_turn()
    turn_2_monster_id = combat_manager.current_monster_id

    conditions = [
        turn_0_monster_id == "MONSTER_2",
        turn_1_monster_id == "MONSTER_0",
        turn_2_monster_id == "MONSTER_2",
    ]

    assert all(conditions)
