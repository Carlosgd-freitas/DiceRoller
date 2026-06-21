"""Tests for combat turn management."""

from typing import Dict

from src.combat.manager import CombatManager, OrderStrategy
from tests.utils import assert_conditions


def test_turn_order_faster(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_manager.order_strategy = OrderStrategy.FASTER
    combat_manager.start_combat()

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_3",
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[2].local_id == "MONSTER_2",
        combat_manager.order[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_turn_order_set(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_manager.order_strategy = OrderStrategy.SET
    combat_manager.start_combat()

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        combat_manager.order[1].local_id == "MONSTER_2",
        combat_manager.order[2].local_id == "MONSTER_3",
        combat_manager.order[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_turn_order_shuffle(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_manager.order_strategy = OrderStrategy.SHUFFLE
    combat_manager.start_combat()

    combat_order = set()
    for monster in combat_manager.order:
        combat_order.add(monster.local_id)

    conditions = [combat_order == {"MONSTER_1", "MONSTER_2", "MONSTER_3", "MONSTER_4"}]

    assert_conditions(conditions)


def test_turn_order_slower(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_manager.order_strategy = OrderStrategy.SLOWER
    combat_manager.start_combat()

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_2",
        combat_manager.order[1].local_id == "MONSTER_4",
        combat_manager.order[2].local_id == "MONSTER_1",
        combat_manager.order[3].local_id == "MONSTER_3",
    ]

    assert_conditions(conditions)
