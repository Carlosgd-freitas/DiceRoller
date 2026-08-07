"""Tests for effect with 'OFFENSIVE' type."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.pierce import PierceEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_attack_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect = AttackEffect(Stat(flat=6))

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 4,
        len(monster_2.effects) == 0,
    ]

    effect = AttackEffect(Stat(percent=0.1))

    monster_2.hp = 20

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 5,
        ]
    )

    effect = AttackEffect(Stat(flat=1, percent=1.0))

    monster_2.hp = monster_2.max_hp

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 0,
        ]
    )

    assert_conditions(conditions)


def test_drain_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    drain_effect = DrainEffect(Stat(flat=3))
    block_effect = BlockEffect(Stat(flat=1))

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    effect_manager.execute_effect(
        drain_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        monster_1.hp == 3,
        len(monster_1.effects) == 0,
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 8,
        len(monster_2.effects) == 0,
    ]

    drain_effect = DrainEffect(Stat(percent=0.1))

    effect_manager.execute_effect(
        drain_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_1.hp == 11,
            monster_2.hp == 0,
        ]
    )

    drain_effect = DrainEffect(Stat(flat=1, percent=1.0))

    monster_2.hp = monster_2.max_hp

    effect_manager.execute_effect(
        drain_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_1.hp == monster_1.max_hp,
            monster_2.hp == 0,
        ]
    )

    assert_conditions(conditions)


def test_pierce_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    pierce_effect = PierceEffect(Stat(flat=6))
    block_effect = BlockEffect(Stat(flat=100))

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 4,
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        monster_2.get_effect(Keyword.BLOCK).value == (Stat(flat=100)),
    ]

    pierce_effect = PierceEffect(Stat(percent=0.1))

    monster_2.hp = 20

    effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 5,
            len(monster_2.effects) == 1,
            monster_2.get_effect(Keyword.BLOCK).value == (Stat(flat=100)),
        ]
    )

    pierce_effect = PierceEffect(Stat(flat=1, percent=1.0))

    monster_2.hp = monster_2.max_hp

    effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 0,
            len(monster_2.effects) == 1,
            monster_2.get_effect(Keyword.BLOCK).value == (Stat(flat=100)),
        ]
    )

    assert_conditions(conditions)
