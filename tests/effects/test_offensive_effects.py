"""Tests for offensive effects processing."""

from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.pierce import PierceEffect
from tests.utils import assert_conditions


def test_keyword_attack(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect = AttackEffect(6)

    combat_manager.execute_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        combat_manager.order[2].hp == 4,
    ]

    assert_conditions(conditions)


def test_keyword_drain(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    drain_effect = DrainEffect(3)
    block_effect = BlockEffect(1)

    combat_manager.execute_effect(
        block_effect,
        source=combat_manager.order[2],
        target=combat_manager.order[2],
    )

    combat_manager.execute_effect(
        drain_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        combat_manager.order[2].hp == 8,
        combat_manager.order[2].get_effect(Keyword.BLOCK) is None,
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[1].hp == 3,
    ]

    assert_conditions(conditions)


def test_keyword_pierce(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    pierce_effect = PierceEffect(2)
    block_effect = BlockEffect(6)

    combat_manager.execute_effect(
        block_effect,
        source=combat_manager.order[2],
        target=combat_manager.order[2],
    )

    combat_manager.execute_effect(
        pierce_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        combat_manager.order[2].hp == 8,
        combat_manager.order[2].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[2].get_effect(Keyword.BLOCK).value == 6,
    ]

    assert_conditions(conditions)
