"""Tests for deterioration effects processing."""

from typing import Dict

from src.combat.manager import CombatManager
from src.effects.block import BlockEffect
from src.effects.curse import CurseEffect
from tests.utils import assert_conditions


def test_keyword_curse(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    curse_effect = CurseEffect(6)
    block_effect = BlockEffect(6)

    combat_manager.execute_effect(
        block_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    combat_manager.execute_effect(
        curse_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[1].hp == 0,
    ]

    assert_conditions(conditions)
