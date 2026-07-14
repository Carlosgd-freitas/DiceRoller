"""Tests for combat softlocks."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.manager import CombatManager, CombatStatus


def test_check_softlock(combat_softlock: Dict):
    combat_manager: CombatManager = combat_softlock["combat_manager"]
    monsters: List[Monster] = combat_softlock["monsters"]

    conditions = [
        combat_manager.softlock_count == 0,
        combat_manager.get_combat_status()["status"] == "ONGOING",
    ]

    for turn in range(len(monsters)):
        combat_manager.take_turn()
        combat_manager.end_turn()
        if turn < len(monsters) - 1:
            combat_manager.next_turn()
    combat_manager.end_round()

    conditions.extend(
        [
            combat_manager.softlock_count == 1,
            combat_manager.get_combat_status()["status"] == "ONGOING",
        ]
    )

    monsters[0].hp += 1
    combat_manager.check_softlock()

    conditions.extend(
        [
            combat_manager.softlock_count == 0,
            combat_manager.get_combat_status()["status"] == "ONGOING",
        ]
    )

    assert_conditions(conditions)


def test_softlock_draw(combat_softlock: Dict):
    combat_manager: CombatManager = combat_softlock["combat_manager"]
    monsters: List[Monster] = combat_softlock["monsters"]

    conditions = [
        combat_manager.softlock_count == 0,
        combat_manager.get_combat_status()["status"] == "ONGOING",
    ]

    combat_statuses: List[CombatStatus] = []
    softlock_counts: List[int] = []

    for _ in range(3):
        for _ in range(len(monsters)):
            combat_manager.take_turn()
            combat_manager.end_turn()
            combat_manager.next_turn()
        combat_manager.end_round()

        softlock_counts.append(combat_manager.softlock_count)
        combat_statuses.append(combat_manager.check_combat_status()["status"])

    conditions = [
        combat_statuses == ["ONGOING", "ONGOING", "DRAW"],
        softlock_counts == [1, 2, 3],
    ]

    assert_conditions(conditions)
