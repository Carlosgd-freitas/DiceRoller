"""Tests for defensive effects processing."""

from src.base.effect import Effect
from src.base.keywords import Keyword
from tests.utils import assert_conditions
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_block(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    attack_effect_1 = Effect(Keyword.ATTACK, 3)
    attack_effect_2 = Effect(Keyword.ATTACK, 4)
    block_effect = Effect(Keyword.BLOCK, 6)

    _ = process_effect(
        block_effect,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,

        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 6,

        combat_manager.order[1].get_effect(Keyword.BLOCK) == None,
    ]

    _ = process_effect(
        attack_effect_1,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions.extend([
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 5,

        combat_manager.order[0].get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        combat_manager.order[0].get_effect(Keyword.BLOCK).value == 3,
    ])

    _ = process_effect(
        attack_effect_2,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions.extend([
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 4, ##

        combat_manager.order[0].get_effect(Keyword.BLOCK) == None,
    ])

    assert_conditions(conditions)
