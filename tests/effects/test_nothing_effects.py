"""Tests for nothing effects processing."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Dict

from src.effects.nothing import NothingEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_nothing_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]
    before = deepcopy(monster)

    effect = NothingEffect()

    effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions = [
        monster.is_equivalent(before),
    ]

    assert_conditions(conditions)
