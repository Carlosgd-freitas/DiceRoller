"""Tests for stacking effects."""

from __future__ import annotations

from math import isclose
from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
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

    effect_0 = BurnEffect(value=1, duration=3, decay=5, accuracy=0.8)
    effect_1 = BurnEffect(value=2, duration=4, decay=6, accuracy=0.7)

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    stacked_effect: BurnEffect = monster.get_effect(Keyword.BURN)

    conditions = [
        isinstance(stacked_effect, BurnEffect),
        len(monster.effects) == 1,
        stacked_effect.keyword == Keyword.BURN,
        stacked_effect.value == 3,
        stacked_effect.duration == 4,
        stacked_effect.decay == 11,
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

    effect_0 = ImmunityEffect(effects=[Keyword.BURN, Keyword.BLIND])
    effect_1 = ImmunityEffect(effects=[Keyword.BURN, Keyword.POISON])

    monster.apply_effect(effect_0)
    monster.apply_effect(effect_1)

    stacked_effect: ImmunityEffect = monster.get_effect(Keyword.IMMUNITY)

    conditions = [
        isinstance(stacked_effect, ImmunityEffect),
        len(monster.effects) == 1,
        stacked_effect.keyword == Keyword.IMMUNITY,
        len(stacked_effect.effects) == 3,
        set(stacked_effect.effects) == {Keyword.BURN, Keyword.BLIND, Keyword.POISON},
    ]

    assert_conditions(conditions)
