"""Tests for effect with 'DETERIORATION' type."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
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


def test_corrupt_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]

    corrupt_effect = CorruptEffect(Stat(flat=2))

    monster.effects = [
        ManaRegenEffect(),
        BleedEffect(),
        RegenEffect(removable=False),
        ThornsEffect(),
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


def test_execute_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_4: Monster = combat["monsters"][4]

    effect = ExecuteEffect(Stat(percent=0.5))
    monster_4.hp = 100

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_4,
    )

    conditions = [
        monster_4.is_alive() is False,
        monster_4.hp == 0,
        len(monster_4.effects) == 0,
    ]

    effect = ExecuteEffect(Stat(flat=30))
    monster_4.hp = 30

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.is_alive() is False,
            monster_4.hp == 0,
            len(monster_4.effects) == 0,
        ]
    )

    effect = ExecuteEffect(Stat(flat=2, percent=0.25))
    monster_4.hp = 52

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.is_alive() is False,
            monster_4.hp == 0,
            len(monster_4.effects) == 0,
        ]
    )

    monster_4.hp = 53

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.is_alive() is True,
            monster_4.hp == 53,
            len(monster_4.effects) == 0,
        ]
    )

    assert_conditions(conditions)
