"""Tests for restoration effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
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


def test_cleanse_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]

    cleanse_effect = CleanseEffect(Stat(flat=2))

    monster.effects = [
        BleedEffect(),
        RegenEffect(),
        BurnEffect(removable=False),
        PoisonEffect(),
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


def test_heal_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]
    monster_4.hp = 1

    effect = HealEffect(Stat(flat=9))

    effect_manager.execute_effect(
        effect,
        source=monster_4,
        target=monster_4,
    )

    conditions = [
        monster_4.local_id == "MONSTER_4",
        monster_4.is_alive() is True,
        monster_4.hp == 10,
        len(monster_4.effects) == 0,
    ]

    effect = HealEffect(Stat(percent=0.1))

    effect_manager.execute_effect(
        effect,
        source=monster_4,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.hp == 30,
        ]
    )

    effect = HealEffect(Stat(flat=110, percent=0.5))

    effect_manager.execute_effect(
        effect,
        source=monster_4,
        target=monster_4,
    )

    conditions.extend(
        [
            monster_4.hp == 200,
        ]
    )

    effect_manager.execute_effect(
        effect,
        source=monster_0,
        target=monster_0,
    )

    conditions.extend(
        [
            monster_0.local_id == "MONSTER_0",
            monster_0.is_alive() is False,
            monster_0.hp == 0,
        ]
    )

    assert_conditions(conditions)


def test_mana_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][1]

    effect = ManaEffect(Stat(flat=2))

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

    effect = ManaEffect(Stat(percent=0.5))

    effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.mana == 3,
            len(monster.effects) == 0,
        ]
    )

    assert_conditions(conditions)


def test_revive_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]
    monster_3: Monster = combat["monsters"][3]

    effect = ReviveEffect(Stat(flat=10))

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions = [
        monster_0.is_alive() is True,
        monster_0.hp == 10,
        len(monster_1.effects) == 0,
    ]

    monster_0.hp = 0
    effect = ReviveEffect(Stat(percent=0.25))

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions.extend(
        [
            monster_0.is_alive() is True,
            monster_0.hp == 25,
            len(monster_1.effects) == 0,
        ]
    )

    monster_0.hp = 0
    effect = ReviveEffect(Stat(flat=60, percent=0.5))

    effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions.extend(
        [
            monster_0.is_alive() is True,
            monster_0.hp == 100,
            len(monster_1.effects) == 0,
        ]
    )

    effect_manager.execute_effect(
        effect,
        source=monster_3,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_3.is_alive() is True,
            monster_3.hp == 100,
            len(monster_0.effects) == 0,
        ]
    )

    assert_conditions(conditions)
