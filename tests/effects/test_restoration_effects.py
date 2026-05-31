"""Tests for restoration effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_heal(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["teams"][0][1]

    effect = HealEffect(6)

    conditions = [
        monster.local_id == "MONSTER_1",
        monster.hp == 1,
    ]

    effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.hp == 7,
        ]
    )

    assert_conditions(conditions)


def test_keyword_mana(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["teams"][0][1]

    effect = ManaEffect(2)

    conditions = [
        monster.local_id == "MONSTER_1",
        monster.mana == 0,
    ]

    effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.mana == 2,
        ]
    )

    assert_conditions(conditions)
