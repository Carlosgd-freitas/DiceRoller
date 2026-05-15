"""Tests for defensive effects processing."""

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_keyword_absorb(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    attack_effect_1 = AttackEffect(3)
    attack_effect_2 = AttackEffect(4)
    absorb_effect = AbsorbEffect(6)

    combat_manager.order[0].apply_effect(absorb_effect)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,
        combat_manager.order[0].get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
        combat_manager.order[0].get_effect(Keyword.ABSORB).value == 6,
        combat_manager.order[1].get_effect(Keyword.ABSORB) is None,
    ]

    combat_manager.activate_effect(
        attack_effect_1,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend(
        [
            combat_manager.order[0].local_id == "MONSTER_0",
            combat_manager.order[0].hp == 8,
            combat_manager.order[0].get_effect(Keyword.ABSORB).keyword
            == Keyword.ABSORB,
            combat_manager.order[0].get_effect(Keyword.ABSORB).value == 3,
        ]
    )

    combat_manager.activate_effect(
        attack_effect_2,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend(
        [
            combat_manager.order[0].local_id == "MONSTER_0",
            combat_manager.order[0].hp == 9,
            combat_manager.order[0].get_effect(Keyword.ABSORB) is None,
        ]
    )

    assert_conditions(conditions)


def test_keyword_block(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    attack_effect_1 = AttackEffect(3)
    attack_effect_2 = AttackEffect(4)
    block_effect = BlockEffect(6)

    combat_manager.order[0].apply_effect(block_effect)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,
        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 6,
        combat_manager.order[1].get_effect(Keyword.BLOCK) is None,
    ]

    combat_manager.activate_effect(
        attack_effect_1,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend(
        [
            combat_manager.order[0].local_id == "MONSTER_0",
            combat_manager.order[0].hp == 5,
            combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            combat_manager.order[0].get_effect(Keyword.BLOCK).value == 3,
        ]
    )

    combat_manager.activate_effect(
        attack_effect_2,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend(
        [
            combat_manager.order[0].local_id == "MONSTER_0",
            combat_manager.order[0].hp == 4,
            combat_manager.order[0].get_effect(Keyword.BLOCK) is None,
        ]
    )

    assert_conditions(conditions)
