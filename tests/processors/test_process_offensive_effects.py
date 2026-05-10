"""Tests for offensive effects processing."""

from src.base.effect import Effect
from src.base.keywords import Keyword
from tests.utils import assert_conditions
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_attack(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = Effect(Keyword.ATTACK, 6)

    targets = process_effect(
        effect,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        len(targets) == 1,

        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert_conditions(conditions)


def test_keyword_curse(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = Effect(Keyword.CURSE, 6)

    targets = process_effect(
        effect,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        len(targets) == 1,

        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert_conditions(conditions)


def test_keyword_pierce(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    pierce_effect = Effect(Keyword.PIERCE, 2)
    block_effect = Effect(Keyword.BLOCK, 6)

    _ = process_effect(
        block_effect,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        pierce_effect,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 3,

        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 6,
    ]

    assert_conditions(conditions)
