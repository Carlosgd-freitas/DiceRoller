"""Tests for Entity class."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.entity import Entity
from src.base.keywords import Keyword
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_entity_is_equivalent():
    effect = AttackEffect(Stat(flat=1))
    side = Side(effects=[effect])
    dice = Dice(sides=[side])

    entity_0 = Entity(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    entity_1 = Entity(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    entity_2 = Entity(
        global_id="ID_1",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    conditions = [
        entity_0.is_equivalent(entity_0) is True,
        entity_0.is_equivalent(entity_1) is True,
        entity_0.is_equivalent(entity_2) is False,
    ]

    assert_conditions(conditions)


def test_entity_roll_single():
    side = Side(effects=[AttackEffect(Stat(flat=1))])

    dice = Dice(sides=[side])

    entity = Entity(dice=[dice])

    picked_sides = entity.roll()

    conditions = [
        len(picked_sides) == 1,
        picked_sides[0].effects[0].keyword == Keyword.ATTACK,
        picked_sides[0].effects[0].value == Stat(flat=1, percent=None),
    ]

    assert_conditions(conditions)


def test_entity_roll_multiple():
    side_0 = Side(effects=[AttackEffect(Stat(flat=1))])

    dice_0 = Dice(
        sides=[
            side_0,
        ]
    )

    side_1 = Side(effects=[BlockEffect(Stat(flat=2))])

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
        picked_sides[0].effects[0].value == Stat(flat=1, percent=None),
        picked_sides[1].effects[0].keyword == Keyword.BLOCK,
        picked_sides[1].effects[0].value == Stat(flat=2, percent=None),
    ]

    assert_conditions(conditions)
