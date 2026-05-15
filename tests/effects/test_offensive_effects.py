"""Tests for offensive effects processing."""

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.curse import CurseEffect
from src.effects.drain import DrainEffect
from src.effects.pierce import PierceEffect
from tests.utils import assert_conditions


def test_keyword_attack(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = AttackEffect(6)

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert_conditions(conditions)


def test_keyword_curse(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = CurseEffect(6)

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert_conditions(conditions)


def test_keyword_drain(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    drain_effect = DrainEffect(3)
    block_effect = BlockEffect(1)

    combat_manager.order[0].apply_effect(block_effect)

    combat_manager.activate_effect(
        drain_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 3,
        combat_manager.order[0].get_effect(Keyword.BLOCK) is None,
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[1].hp == 7,
    ]

    assert_conditions(conditions)


def test_keyword_pierce(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    pierce_effect = PierceEffect(2)
    block_effect = BlockEffect(6)

    combat_manager.order[0].apply_effect(block_effect)

    combat_manager.activate_effect(
        pierce_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 3,
        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 6,
    ]

    assert_conditions(conditions)
