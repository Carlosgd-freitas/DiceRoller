"""Tests for combat turn management."""

from typing import Dict

from src.combat.manager import CombatManager, OrderStrategy
from tests.utils import assert_conditions


def test_next_turn(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.order_strategy = OrderStrategy.FASTER
    combat_manager.start_combat()

    turns_monster_id = []

    for _ in range(5):
        turn_monster_id = combat_manager.current_monster.local_id
        turns_monster_id.append(turn_monster_id)
        combat_manager.next_turn()

    conditions = [
        turns_monster_id[0] == "MONSTER_3",
        turns_monster_id[1] == "MONSTER_1",
        turns_monster_id[2] == "MONSTER_2",
        turns_monster_id[3] == "MONSTER_4",
        turns_monster_id[4] == "MONSTER_3",
    ]

    assert_conditions(conditions)
