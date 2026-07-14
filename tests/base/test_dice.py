"""Tests for Dice class."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_dice_is_equivalent():
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

    dice_0 = Dice(sides=[deepcopy(side_0)])
    dice_1 = Dice(sides=[deepcopy(side_0)])
    dice_2 = Dice(sides=[deepcopy(side_1)])

    conditions = [
        dice_0.is_equivalent(dice_0) is True,
        dice_0.is_equivalent(dice_1) is True,
        dice_0.is_equivalent(dice_2) is False,
    ]

    assert_conditions(conditions)


def test_dice_roll_single():
    side = Side(effects=[AttackEffect(1)])

    dice = Dice(sides=[side])

    picked_side = dice.roll()

    conditions = [
        picked_side.effects[0].keyword == Keyword.ATTACK,
        picked_side.effects[0].value == 1,
    ]

    assert_conditions(conditions)


def test_dice_roll_multiple():
    side_0 = Side(effects=[BlockEffect(2)], weight=0)

    side_1 = Side(effects=[AttackEffect(1)], weight=1)

    dice = Dice(
        sides=[
            side_0,
            side_1,
        ]
    )

    picked_side = dice.roll()

    conditions = [
        picked_side.effects[0].keyword == Keyword.ATTACK,
        picked_side.effects[0].value == 1,
    ]

    assert_conditions(conditions)
