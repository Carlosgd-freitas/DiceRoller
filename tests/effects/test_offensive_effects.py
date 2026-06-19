"""Tests for offensive effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.pierce import PierceEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_attack(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    effect = AttackEffect(6)

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 4,
        len(monster_2.effects) == 0,
    ]

    assert_conditions(conditions)


def test_keyword_drain(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    drain_effect = DrainEffect(3)
    block_effect = BlockEffect(1)

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
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 8,
        len(monster_2.effects) == 0,
        monster_1.local_id == "MONSTER_1",
        monster_1.hp == 3,
        len(monster_1.effects) == 0,
    ]

    assert_conditions(conditions)


def test_keyword_pierce(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    pierce_effect = PierceEffect(2)
    block_effect = BlockEffect(6)

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
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 8,
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        monster_2.get_effect(Keyword.BLOCK).value == 6,
        len(monster_1.effects) == 0,
    ]

    assert_conditions(conditions)
