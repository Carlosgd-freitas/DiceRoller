"""Tests for Side class."""

from base.side import Side
from base.effect import Effect
from base.keywords import Keyword


def test_get_effects_single():
    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 1),
            Effect(Keyword.ATTACK, 2),
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
        effects[0][1].value == 2
    ]
    
    assert all(conditions)


def test_get_effects_multiple():
    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 1),
            Effect(Keyword.BLOCK, 1),
            Effect(Keyword.ATTACK, 2),
            Effect(Keyword.BLOCK, 2),
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
        effects[1][1].value == 2
    ]
    
    assert all(conditions)
