"""Tests for effect with 'UTILITY' type."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.combat.manager import CombatManager
from src.effects.burn import BurnEffect
from src.effects.delay import DelayEffect
from src.effects.strength import StrengthEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster


def test_delay_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.current_monster = monster_2

    effect_burn = BurnEffect(Stat(flat=1, percent=0), duration=1)
    effect_delay = DelayEffect(Stat(flat=1, percent=0), target_keywords=[Keyword.ALL])
    effect_strength = StrengthEffect(Stat(flat=1, percent=0), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_burn,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_strength,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_delay,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 2,
        monster_2.get_effect(Keyword.BURN).keyword == Keyword.BURN,
        monster_2.get_effect(Keyword.BURN).duration == 2,
        monster_2.get_effect(Keyword.STRENGTH).keyword == Keyword.STRENGTH,
        monster_2.get_effect(Keyword.STRENGTH).duration == 2,
    ]

    effect_delay = DelayEffect(Stat(flat=0, percent=1), target_keywords=[Keyword.ALL])

    combat_manager.effect_manager.execute_effect(
        effect_delay,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 2,
            monster_2.get_effect(Keyword.BURN).duration == 4,
            monster_2.get_effect(Keyword.STRENGTH).duration == 4,
        ]
    )

    effect_delay = DelayEffect(Stat(flat=1, percent=0.5), target_keywords=[Keyword.ALL])

    combat_manager.effect_manager.execute_effect(
        effect_delay,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 2,
            monster_2.get_effect(Keyword.BURN).duration == 7,
            monster_2.get_effect(Keyword.STRENGTH).duration == 7,
        ]
    )

    effect_delay = DelayEffect(
        Stat(flat=1, percent=0), target_keywords=[Keyword.STRENGTH]
    )

    combat_manager.effect_manager.execute_effect(
        effect_delay,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 2,
            monster_2.get_effect(Keyword.BURN).duration == 7,
            monster_2.get_effect(Keyword.STRENGTH).duration == 8,
        ]
    )

    effect_delay = DelayEffect(Stat(flat=1, percent=1))

    combat_manager.effect_manager.execute_effect(
        effect_delay,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 2,
            monster_2.get_effect(Keyword.BURN).duration == 7,
            monster_2.get_effect(Keyword.STRENGTH).duration == 8,
        ]
    )

    assert_conditions(conditions)
