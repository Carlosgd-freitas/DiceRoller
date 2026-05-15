"""Tests for Side class."""

from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect


def test_side_get_effects_single():
    side = Side(
        effects=[
            AttackEffect(1),
            AttackEffect(2),
        ]
    )

    effects = side.get_effects(
        keyword=Keyword.ATTACK,
        value=2,
    )

    conditions = [
        len(effects) == 1,
        effects[0][0] == 1,
        effects[0][1].keyword == Keyword.ATTACK,
        effects[0][1].value == 2,
    ]

    assert all(conditions)


def test_side_get_effects_multiple():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(1),
            AttackEffect(2),
            BlockEffect(2),
        ]
    )

    effects = side.get_effects(
        keyword=Keyword.ATTACK,
    )

    conditions = [
        len(effects) == 2,
        effects[0][0] == 0,
        effects[0][1].keyword == Keyword.ATTACK,
        effects[0][1].value == 1,
        effects[1][0] == 2,
        effects[1][1].keyword == Keyword.ATTACK,
        effects[1][1].value == 2,
    ]

    assert all(conditions)
