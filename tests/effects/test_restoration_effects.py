"""Tests for restoration effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.effects.bleed import BleedEffect
from src.effects.burn import BurnEffect
from src.effects.cleanse import CleanseEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.revive import ReviveEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_keyword_cleanse(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["monsters"][1]

    cleanse_effect = CleanseEffect(2)

    monster.effects = [
        BleedEffect(1),
        RegenEffect(1),
        BurnEffect(1, removable=False),
        PoisonEffect(1),
    ]

    conditions = [
        monster.local_id == "MONSTER_1",
        len(monster.effects) == 4,
    ]

    effect_manager.execute_effect(
        cleanse_effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            len(monster.effects) == 2,
            monster.get_effect(Keyword.BURN).keyword == Keyword.BURN,
            monster.get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        ]
    )

    assert_conditions(conditions)


def test_keyword_heal(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["monsters"][1]

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
            len(monster.effects) == 0,
        ]
    )

    assert_conditions(conditions)


def test_keyword_mana(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster: Monster = managers["monsters"][1]

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
            len(monster.effects) == 0,
        ]
    )

    assert_conditions(conditions)


def test_keyword_revive(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_0: Monster = managers["monsters"][0]
    monster_1: Monster = managers["monsters"][1]

    effect = ReviveEffect(0.25)

    conditions = [
        monster_0.local_id == "MONSTER_0",
        monster_0.hp == 0,
        not monster_0.is_alive(),
    ]

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions.extend(
        [
            monster_0.hp == 25,
            monster_0.is_alive(),
            len(monster_0.effects) == 0,
        ]
    )

    assert_conditions(conditions)
