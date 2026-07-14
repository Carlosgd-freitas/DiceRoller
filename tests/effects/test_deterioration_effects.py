"""Tests for deterioration effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.effects.bleed import BleedEffect
from src.effects.corrupt import CorruptEffect
from src.effects.execute import ExecuteEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.regen import RegenEffect
from src.effects.thorns import ThornsEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_corrupt(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]

    corrupt_effect = CorruptEffect(2)

    monster.effects = [
        ManaRegenEffect(1),
        BleedEffect(1),
        RegenEffect(1, removable=False),
        ThornsEffect(1),
    ]

    conditions = [
        monster.local_id == "MONSTER_1",
        len(monster.effects) == 4,
    ]

    effect_manager.execute_effect(
        corrupt_effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            len(monster.effects) == 2,
            monster.get_effect(Keyword.BLEED).keyword == Keyword.BLEED,
            monster.get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        ]
    )

    assert_conditions(conditions)


def test_keyword_execute(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_4: Monster = combat["monsters"][4]

    execute_effect = ExecuteEffect(value_percent=0.5)

    effect_manager.execute_effect(
        execute_effect,
        source=monster_1,
        target=monster_4,
    )

    conditions = [
        monster_4.local_id == "MONSTER_4",
        monster_4.hp == 200,
        len(monster_4.effects) == 0,
    ]

    monster_4.hp = 100

    effect_manager.execute_effect(
        execute_effect,
        source=monster_1,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.hp == 0,
            len(monster_4.effects) == 0,
        ]
    )

    assert_conditions(conditions)
