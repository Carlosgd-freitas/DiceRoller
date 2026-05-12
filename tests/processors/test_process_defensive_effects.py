"""Tests for defensive effects processing."""

from src.base.keywords import Keyword
from src.effects.block import BlockEffect
from tests.utils import assert_conditions
from src.effects.attack import AttackEffect
from src.combat.manager import CombatManager


def test_keyword_block(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    attack_effect_1 = AttackEffect(3)
    attack_effect_2 = AttackEffect(4)
    block_effect = BlockEffect(6)

    combat_manager.order[0].add_effect(block_effect)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,

        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 6,

        combat_manager.order[1].get_effect(Keyword.BLOCK) == None,
    ]

    attack_effect_1.activate(
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend([
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,

        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 3,
    ])

    attack_effect_2.activate(
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions.extend([
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 4,

        combat_manager.order[0].get_effect(Keyword.BLOCK) == None,
    ])

    assert_conditions(conditions)
