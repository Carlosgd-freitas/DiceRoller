"""Tests for combat turn management."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Dict

from src.base.stat import Stat
from src.effects.bleed import BleedEffect
from src.effects.burn import BurnEffect
from src.effects.poison import PoisonEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.manager import CombatManager


def test_end_turn_decay_effects(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    combat_manager.start_combat()

    combat_manager.order[0].effects = [
        BleedEffect(
            value=Stat(flat=5),
            duration=2,
            delta=Stat(flat=1),
        ),
        BurnEffect(
            value=Stat(flat=10),
            duration=4,
            delta=Stat(flat=-5),
        ),
        PoisonEffect(
            value=Stat(flat=8),
            duration=3,
            delta=Stat(percent=-0.5),
        ),
    ]

    effects_by_turn = [deepcopy(combat_manager.order[0].effects)]

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    combat_manager.end_turn()
    effects_by_turn.append(deepcopy(combat_manager.order[0].effects))

    conditions = [
        effects_by_turn[0][0].value == Stat(flat=5, percent=None),
        effects_by_turn[0][1].value == Stat(flat=10, percent=None),
        effects_by_turn[0][2].value == Stat(flat=8, percent=None),
        effects_by_turn[1][0].value == Stat(flat=6, percent=None),
        effects_by_turn[1][1].value == Stat(flat=5, percent=None),
        effects_by_turn[1][2].value == Stat(flat=4, percent=None),
        effects_by_turn[2][0].value == Stat(flat=0, percent=None),
        effects_by_turn[2][1].value == Stat(flat=2, percent=None),
        effects_by_turn[3][0].value == Stat(flat=-5, percent=None),
    ]

    assert_conditions(conditions)


def test_end_turn_remove_effects(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    combat_manager.start_combat()

    combat_manager.order[0].effects = [
        BleedEffect(
            value=Stat(flat=5),
            duration=2,
            delta=Stat(flat=1),
        ),
        BurnEffect(
            value=Stat(flat=10),
            duration=4,
            delta=Stat(flat=-5),
        ),
        PoisonEffect(
            value=Stat(flat=10),
            duration=3,
            delta=Stat(percent=-0.1),
        ),
    ]

    effects_by_turn = [deepcopy(combat_manager.order[0].effects)]

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
        len(effects_by_turn[0]) == 3,
        effects_by_turn[0][0].duration == 2,
        effects_by_turn[0][1].duration == 4,
        effects_by_turn[0][2].duration == 3,
        len(effects_by_turn[1]) == 3,
        effects_by_turn[1][0].duration == 1,
        effects_by_turn[1][1].duration == 3,
        effects_by_turn[1][2].duration == 2,
        len(effects_by_turn[2]) == 2,
        effects_by_turn[2][0].duration == 2,
        effects_by_turn[2][1].duration == 1,
        len(effects_by_turn[3]) == 1,
        effects_by_turn[3][0].duration == 1,
        len(effects_by_turn[4]) == 0,
        len(effects_by_turn[5]) == 0,
    ]

    assert_conditions(conditions)
