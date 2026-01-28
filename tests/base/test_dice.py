"""Tests for Dice class."""

from src.base.side import Side
from src.base.dice import Dice
from src.base.effect import Effect
from src.base.keywords import Keyword


def test_dice_roll_single():
    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 1)
        ]
    )

    dice = Dice(
        sides=[
            side
        ]
    )

    picked_side = dice.roll()
    
    conditions = [
        picked_side.effects[0].keyword == Keyword.ATTACK,
        picked_side.effects[0].value == 1,
    ]
    
    assert all(conditions)


def test_dice_roll_multiple():
    side_0 = Side(
        effects=[
            Effect(Keyword.BLOCK, 2)
        ], weight = 0
    )

    side_1 = Side(
        effects=[
            Effect(Keyword.ATTACK, 1)
        ], weight = 1
    )

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
    
    assert all(conditions)
