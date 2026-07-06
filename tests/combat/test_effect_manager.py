"""Tests for EffectManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.dice import Dice
from src.base.side import Side
from src.base.triggers import Trigger
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_effect_manager_process_trigger(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    try:
        effect_manager.process_trigger(
            Trigger.BEING_ATTACKED,
            source=monster_2,
            target=monster_1,
        )
        suceeded = True
    except Exception:
        suceeded = False

    conditions = [
        suceeded is True,
    ]

    assert_conditions(conditions)


def test_effect_manager_execute_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    effect = AttackEffect(1)

    executed = effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        executed is True,
        monster_1.local_id == "MONSTER_1",
        monster_2.local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_effect_manager_roll(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster: Monster = combat["monsters"][0]
    dice_0 = Dice(sides=[Side(effects=[AttackEffect(1)])])
    dice_1 = Dice(sides=[Side(effects=[BlockEffect(1)])])

    monster.dice = [dice_0, dice_1]

    rolled = effect_manager.roll(monster)

    conditions = [
        len(rolled) == 2,
        isinstance(rolled[0], Side),
        isinstance(rolled[1], Side),
    ]

    assert_conditions(conditions)
