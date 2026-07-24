"""Tests for healing procesing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.stat import Stat
from src.effects.heal import HealEffect
from src.processors.healing import calculate_healing
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster


def test_calculate_healing_absolute(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    effect = HealEffect(Stat(flat=9))

    healed = calculate_healing(
        effect,
        monster_1,
        monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 0,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        healed == 9,
    ]

    assert_conditions(conditions)


def test_calculate_healing_percent(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    effect = HealEffect(Stat(percent=0.25))

    healed = calculate_healing(
        effect,
        monster_1,
        monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 0,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        healed == 25,
    ]

    assert_conditions(conditions)


def test_calculate_healing_both(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    effect = HealEffect(Stat(flat=20, percent=0.25))

    healed = calculate_healing(
        effect,
        monster_1,
        monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 0,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        healed == 45,
    ]

    assert_conditions(conditions)


def test_calculate_healing_over(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    effect = HealEffect(Stat(flat=80, percent=1))

    healed = calculate_healing(
        effect,
        monster_1,
        monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 0,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        healed == 100,
    ]

    assert_conditions(conditions)
