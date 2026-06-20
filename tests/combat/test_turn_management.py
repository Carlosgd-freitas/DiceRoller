"""Tests for combat turn management."""

from typing import Dict

from src.combat.manager import CombatManager
from tests.utils import assert_conditions


def test_next_turn_simple(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    turn_local_ids = []

    for _ in range(2):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.next_turn()

    conditions = [
        turn_local_ids[0] == "MONSTER_1",
        turn_local_ids[1] == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_next_turn_skip(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.order[1].turn_taken = True
    combat_manager.order[2].turn_taken = True

    turn_local_ids = []

    for _ in range(2):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.next_turn()

    conditions = [
        turn_local_ids[0] == "MONSTER_1",
        turn_local_ids[1] == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_next_turn_wrap(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[3]

    combat_manager.order[1].turn_taken = True
    combat_manager.order[2].turn_taken = True
    combat_manager.order[3].turn_taken = True

    turn_local_ids = []

    for _ in range(2):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.next_turn()

    conditions = [
        turn_local_ids[0] == "MONSTER_4",
        turn_local_ids[1] == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_next_turn_unfound(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    for monster in combat_manager.order:
        monster.turn_taken = True

    turn_local_ids = []

    for _ in range(2):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.next_turn()

    conditions = [
        turn_local_ids[0] == "MONSTER_2",
        turn_local_ids[1] == "MONSTER_2",
    ]

    assert_conditions(conditions)
