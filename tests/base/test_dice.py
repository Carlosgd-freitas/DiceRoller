"""Tests for Dice class."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_dice_is_equivalent():
    effect = AttackEffect(Stat(flat=1))
    side = Side(effects=[effect])

    dice_0 = Dice(sides=[deepcopy(side)])
    dice_1 = Dice(sides=[deepcopy(side)])
    dice_2 = Dice(sides=[deepcopy(side), deepcopy(side)])

    conditions = [
        dice_0.is_equivalent(dice_0) is True,
        dice_0.is_equivalent(dice_1) is True,
        dice_0.is_equivalent(dice_2) is False,
    ]

    assert_conditions(conditions)


def test_dice_roll_single():
    side = Side(effects=[AttackEffect(Stat(flat=1))])

    dice = Dice(sides=[side])

    picked_side = dice.roll()

    conditions = [
        picked_side.effects[0].keyword == Keyword.ATTACK,
        picked_side.effects[0].value == Stat(flat=1, percent=None),
    ]

    assert_conditions(conditions)


def test_dice_roll_multiple():
    side_0 = Side(effects=[BlockEffect(Stat(flat=2))], weight=0)
    side_1 = Side(effects=[AttackEffect(Stat(flat=1))], weight=1)

    dice = Dice(
        sides=[
            side_0,
            side_1,
        ]
    )

    picked_side = dice.roll()

    conditions = [
        picked_side.effects[0].keyword == Keyword.ATTACK,
        picked_side.effects[0].value == Stat(flat=1, percent=None),
    ]

    assert_conditions(conditions)
