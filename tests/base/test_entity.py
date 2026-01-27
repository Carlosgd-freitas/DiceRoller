"""Tests for Entity class."""

from src.base.side import Side
from src.base.dice import Dice
from src.base.effect import Effect
from src.base.entity import Entity
from src.base.keywords import Keyword


def test_entity_roll_single():
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

    entity = Entity(
        dice=[
            dice
        ]
    )

    picked_sides = entity.roll()
    
    conditions = [
        len(picked_sides) == 1,

        picked_sides[0].effects[0].keyword == Keyword.ATTACK,
        picked_sides[0].effects[0].value == 1,
    ]
    
    assert all(conditions)


def test_entity_roll_multiple():
    side_0 = Side(
        effects=[
            Effect(Keyword.ATTACK, 1)
        ]
    )

    dice_0 = Dice(
        sides=[
            side_0,
        ]
    )

    side_1 = Side(
        effects=[
            Effect(Keyword.BLOCK, 2)
        ]
    )

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
    
    assert all(conditions)
