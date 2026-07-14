"""Tests for Side class."""

from copy import deepcopy

from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from tests.utils import assert_conditions


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


def test_side_get_main_effect_type():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
            AbsorbEffect(3),
        ]
    )

    main_effect_type = side.get_main_effect_type()

    conditions = [
        main_effect_type == EffectType.DEFENSIVE,
    ]

    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
        ]
    )

    main_effect_type = side.get_main_effect_type()

    conditions.extend(
        [
            main_effect_type == EffectType.OFFENSIVE,
        ]
    )

    side = Side(effects=[])

    main_effect_type = side.get_main_effect_type()

    conditions.extend(
        [
            main_effect_type is None,
        ]
    )

    assert_conditions(conditions)


def test_side_get_main_keyword():
    side = Side(
        effects=[
            AttackEffect(1),
            BlockEffect(2),
            AbsorbEffect(3),
        ]
    )

    main_keyword = side.get_main_keyword()

    conditions = [
        main_keyword == Keyword.ATTACK,
    ]

    side = Side(
        effects=[
            AbsorbEffect(1),
            BlockEffect(2),
            AbsorbEffect(3),
        ]
    )

    main_keyword = side.get_main_keyword()

    conditions.extend(
        [
            main_keyword == Keyword.ABSORB,
        ]
    )

    side = Side(effects=[])

    main_keyword = side.get_main_keyword()

    conditions.extend(
        [
            main_keyword is None,
        ]
    )

    assert_conditions(conditions)


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


def test_side_is_equivalent():
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

    side_0 = Side(effects=[deepcopy(effect_0)])
    side_1 = Side(effects=[deepcopy(effect_0)])
    side_2 = Side(effects=[deepcopy(effect_1)])

    conditions = [
        side_0.is_equivalent(side_0) is True,
        side_0.is_equivalent(side_1) is True,
        side_0.is_equivalent(side_2) is False,
    ]

    assert_conditions(conditions)
