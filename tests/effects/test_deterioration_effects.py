"""Tests for deterioration effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.effects.block import BlockEffect
from src.effects.curse import CurseEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_curse(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["teams"][0][1]

    curse_effect = CurseEffect(6)
    block_effect = BlockEffect(6)

    effect_manager.execute_effect(
        block_effect,
        source=monster,
        target=monster,
    )

    effect_manager.execute_effect(
        curse_effect,
        source=monster,
        target=monster,
    )

    conditions = [
        monster.local_id == "MONSTER_1",
        monster.hp == 0,
    ]

    assert_conditions(conditions)
