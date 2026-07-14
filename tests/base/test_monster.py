"""Tests for Monster class."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.effects.attack import AttackEffect
from tests.utils import assert_conditions


def test_monster_is_equivalent():
    effect_0 = AttackEffect()
    effect_1 = AttackEffect(
        value=10,
        value_percent=11,
        duration=12,
        decay=13,
        accuracy=0.14,
        removable=False,
        target_keywords=[Keyword.BURN],
    )

    side_0 = Side(effects=[effect_0])
    side_1 = Side(effects=[effect_1])

    dice_0 = Dice(sides=[side_0])
    dice_1 = Dice(sides=[side_1])

    monster_0 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice_0)],
    )

    monster_1 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice_0)],
    )

    monster_2 = Monster(
        global_id="ID_1",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice_1)],
    )

    conditions = [
        monster_0.is_equivalent(monster_0) is True,
        monster_0.is_equivalent(monster_1) is True,
        monster_0.is_equivalent(monster_2) is False,
    ]

    assert_conditions(conditions)
