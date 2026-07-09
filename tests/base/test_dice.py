"""Tests for Dice class."""

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


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
