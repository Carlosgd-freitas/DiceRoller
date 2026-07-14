"""Tests for combat turn management."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.manager import CombatManager


def test_is_round_start(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for monster in combat_manager.order:
        monster.turn_taken = False

    value = combat_manager.is_round_start()

    conditions = [
        value is True,
    ]

    assert_conditions(conditions)


def test_is_round_end(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for monster in combat_manager.order:
        monster.turn_taken = True

    value = combat_manager.is_round_end()

    conditions = [
        value is True,
    ]

    assert_conditions(conditions)


def test_next_turn_simple(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    turn_local_ids = []

    for _ in range(2):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.next_turn()

    conditions = [
        turn_local_ids[0] == "MONSTER_1",
        turn_local_ids[1] == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_next_turn_skip(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

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


def test_next_turn_wrap(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

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


def test_next_turn_unfound(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

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
