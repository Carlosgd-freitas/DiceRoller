"""Tests for stacking effects."""

from __future__ import annotations

from math import isclose
from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.effects.burn import BurnEffect
from src.effects.doom import DoomEffect
from src.effects.immunity import ImmunityEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster


def test_stack_fail(combat: Dict):
    monster: Monster = combat["monsters"][2]

    effect_0 = BurnEffect()
    effect_1 = DoomEffect()

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    conditions = [
        len(monster.effects) == 2,
    ]

    assert_conditions(conditions)


def test_stack_generic_effect(combat: Dict):
    monster: Monster = combat["monsters"][2]

    effect_0 = BurnEffect(
        value=Stat(flat=1, percent=None),
        duration=3,
        delta=Stat(flat=5, percent=0.5),
        accuracy=0.8,
    )
    effect_1 = BurnEffect(
        value=Stat(flat=2, percent=None),
        duration=4,
        delta=Stat(flat=6, percent=0.6),
        accuracy=0.7,
    )

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    stacked_effect: BurnEffect = monster.get_effect(Keyword.BURN)

    conditions = [
        isinstance(stacked_effect, BurnEffect),
        len(monster.effects) == 1,
        stacked_effect.keyword == Keyword.BURN,
        stacked_effect.value.flat == 3,
        stacked_effect.value.percent is None,
        stacked_effect.duration == 4,
        stacked_effect.delta.flat == 11,
        isclose(stacked_effect.delta.percent, 1.1),
        isclose(stacked_effect.accuracy, 0.8),
    ]

    assert_conditions(conditions)


def test_stack_doom_effect(combat: Dict):
    monster: Monster = combat["monsters"][2]

    effect_0 = DoomEffect(duration=13)
    effect_1 = DoomEffect(duration=7)

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    stacked_effect: DoomEffect = monster.get_effect(Keyword.DOOM)

    conditions = [
        isinstance(stacked_effect, DoomEffect),
        len(monster.effects) == 1,
        stacked_effect.keyword == Keyword.DOOM,
        stacked_effect.duration == 7,
    ]

    assert_conditions(conditions)


def test_stack_immunity_effect(combat: Dict):
    monster: Monster = combat["monsters"][2]

    effect_0 = ImmunityEffect(duration=2, target_keywords=[Keyword.BURN, Keyword.BLIND])
    effect_1 = ImmunityEffect(
        duration=4, target_keywords=[Keyword.BURN, Keyword.POISON]
    )

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    stacked_effect = monster.get_effect(Keyword.IMMUNITY)

    conditions = [
        isinstance(stacked_effect, ImmunityEffect),
        len(monster.effects) == 1,
        stacked_effect.keyword == Keyword.IMMUNITY,
        stacked_effect.duration == 4,
        len(stacked_effect.target_keywords) == 3,
        set(stacked_effect.target_keywords)
        == {Keyword.BURN, Keyword.BLIND, Keyword.POISON},
    ]

    assert_conditions(conditions)
