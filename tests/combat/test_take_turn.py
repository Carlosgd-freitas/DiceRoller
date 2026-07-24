"""Tests for turn taking."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.pain import PainEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_effect_interrupt(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    side = Side(
        effects=[
            PainEffect(Stat(flat=100)),
            AttackEffect(Stat(flat=100)),
        ]
    )

    for effect in side.effects:
        effect_manager.execute_effect(
            effect=effect,
            source=monster_2,
            target=monster_1,
        )

    conditions = [
        monster_1.is_alive() is False,
        monster_2.is_alive() is True,
    ]

    assert_conditions(conditions)
