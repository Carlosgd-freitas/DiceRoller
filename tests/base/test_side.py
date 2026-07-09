"""Tests for Side class."""

from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


def test_side_has_effect():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
        ]
    )

    has_effect = side.has_effect(keyword=Keyword.ATTACK)

    conditions = [
        has_effect is True,
    ]

    has_effect = side.has_effect(keyword=Keyword.BURN)

    conditions.extend(
        [
            has_effect is False,
        ]
    )

    assert_conditions(conditions)


def test_side_get_effect():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
        ]
    )

    effect = side.get_effect(keyword=Keyword.ATTACK)

    conditions = [
        effect.keyword == Keyword.ATTACK,
        effect.value == 1,
    ]

    effect = side.get_effect(keyword=Keyword.BURN)

    conditions.extend(
        [
            effect is None,
        ]
    )

    assert_conditions(conditions)


def test_side_get_effect_summary():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
            AbsorbEffect(3),
        ]
    )

    effect_summary = side.get_effect_summary()

    conditions = [
        len(effect_summary) == 2,
        "OFFENSIVE" in effect_summary.keys(),
        effect_summary["OFFENSIVE"] == [Keyword.ATTACK],
        "DEFENSIVE" in effect_summary.keys(),
        effect_summary["DEFENSIVE"] == [Keyword.BLOCK, Keyword.ABSORB],
    ]

    assert_conditions(conditions)
