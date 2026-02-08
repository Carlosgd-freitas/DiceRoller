"""Tests for combat turn management."""

from pytest import fixture
from src.base.monster import Monster
from src.combat.manager import CombatManager


@fixture
def teams():
    monster_0 = Monster(
        local_id="MONSTER_0",
        speed=5,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        speed=1,
    )
    monster_2 = Monster(
        local_id="MONSTER_2",
        speed=10,
    )

    return [
        [monster_0, monster_1],
        [monster_2]
    ]


def test_turn_order_set(teams):
    combat_manager = CombatManager(
        teams=teams,
        order_strategy="SET",
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[2].local_id == "MONSTER_2",
    ]

    assert all(conditions)


def test_turn_order_faster(teams):
    combat_manager = CombatManager(
        teams=teams,
        order_strategy="FASTER",
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_2",
        combat_manager.order[1].local_id == "MONSTER_0",
        combat_manager.order[2].local_id == "MONSTER_1",
    ]

    assert all(conditions)


def test_turn_order_slower(teams):
    combat_manager = CombatManager(
        teams=teams,
        order_strategy="SLOWER",
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        combat_manager.order[1].local_id == "MONSTER_0",
        combat_manager.order[2].local_id == "MONSTER_2",
    ]

    assert all(conditions)
