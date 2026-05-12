"""Tests for combat turn management."""

from copy import deepcopy
from pytest import fixture
from src.base.monster import Monster
from src.combat.manager import CombatManager
from src.effects.nothing import NothingEffect


@fixture
def combat_manager():
    effect_0 = NothingEffect(
        value=5,
        duration=2,
        decay=1,
    )

    effect_1 = NothingEffect(
        value=10,
        duration=4,
        decay=5,
    )

    monster = Monster(
        local_id="MONSTER_0",
        effects=[effect_0, effect_1]
    )

    combat_manager = CombatManager(
        teams=[
            [monster]
        ],
        order_strategy="SET",
    )

    combat_manager.start_combat()

    return combat_manager


def test_end_turn_remove_effects(combat_manager: CombatManager):
    effects_by_turn = [
        deepcopy(combat_manager.order[0].effects)
    ]

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    conditions = [
        len(effects_by_turn[0]) == 2,
        effects_by_turn[0][0].duration == 2,
        effects_by_turn[0][1].duration == 4,

        len(effects_by_turn[1]) == 2,
        effects_by_turn[1][0].duration == 1,
        effects_by_turn[1][1].duration == 3,

        len(effects_by_turn[2]) == 1,
        effects_by_turn[2][0].duration == 2,

        len(effects_by_turn[3]) == 1,
        effects_by_turn[3][0].duration == 1,

        len(effects_by_turn[4]) == 0,

        len(effects_by_turn[5]) == 0,
    ]

    assert all(conditions)


def test_end_turn_decay_effects(combat_manager: CombatManager):
    effects_by_turn = [
        deepcopy(combat_manager.order[0].effects)
    ]

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    conditions = [
        effects_by_turn[0][0].value == 5,
        effects_by_turn[0][1].value == 10,

        effects_by_turn[1][0].value == 4,
        effects_by_turn[1][1].value == 5,

        effects_by_turn[2][0].value == 0,

        effects_by_turn[3][0].value == -5,
    ]

    assert all(conditions)
