"""Tests for curse effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.effects.block import BlockEffect
from src.effects.pain import PainEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_pain(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]

    pain_effect = PainEffect(6)
    block_effect = BlockEffect(6)

    effect_manager.execute_effect(
        block_effect,
        source=monster,
        target=monster,
    )

    effect_manager.execute_effect(
        pain_effect,
        source=monster,
        target=monster,
    )

    conditions = [
        monster.local_id == "MONSTER_1",
        monster.hp == 0,
        len(monster.effects) == 1,
    ]

    assert_conditions(conditions)
