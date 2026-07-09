"""Tests for Entity class."""

from src.base.dice import Dice
from src.base.entity import Entity
from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_entity_roll_single():
    side = Side(effects=[AttackEffect(1)])

    dice = Dice(sides=[side])

    entity = Entity(dice=[dice])

    picked_sides = entity.roll()

    conditions = [
        len(picked_sides) == 1,
        picked_sides[0].effects[0].keyword == Keyword.ATTACK,
        picked_sides[0].effects[0].value == 1,
    ]

    assert_conditions(conditions)


def test_entity_roll_multiple():
    side_0 = Side(effects=[AttackEffect(1)])

    dice_0 = Dice(
        sides=[
            side_0,
        ]
    )

    side_1 = Side(effects=[BlockEffect(2)])

    dice_1 = Dice(
        sides=[
            side_1,
        ]
    )

    entity = Entity(
        dice=[
            dice_0,
            dice_1,
        ]
    )

    picked_sides = entity.roll()

    conditions = [
        len(picked_sides) == 2,
        picked_sides[0].effects[0].keyword == Keyword.ATTACK,
        picked_sides[0].effects[0].value == 1,
        picked_sides[1].effects[0].keyword == Keyword.BLOCK,
        picked_sides[1].effects[0].value == 2,
    ]

    assert_conditions(conditions)
