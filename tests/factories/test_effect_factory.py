"""Tests for EffectFactory class."""

from __future__ import annotations

from math import isclose

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.effects.block import BlockEffect
from src.effects.nothing import NothingEffect
from src.factories.effect import EffectFactory
from tests.utils import assert_conditions


def test_effect_factory_create_simple():
    effect = EffectFactory.create(Keyword.NOTHING)

    conditions = [
        isinstance(effect, NothingEffect),
        effect.keyword == Keyword.NOTHING,
    ]

    assert_conditions(conditions)


def test_effect_factory_create_args():
    effect = EffectFactory.create(
        Keyword.BLOCK,
        value=Stat(flat=2, percent=0.2),
        min_value=Stat(flat=1, percent=0.1),
        max_value=Stat(flat=3, percent=0.3),
        duration=4,
        delta=Stat(flat=5, percent=0.5),
        accuracy=0.6,
        removable=False,
    )

    conditions = [
        isinstance(effect, BlockEffect),
        effect.keyword == Keyword.BLOCK,
        effect.value == Stat(flat=2, percent=0.2),
        effect.min_value == Stat(flat=1, percent=0.1),
        effect.max_value == Stat(flat=3, percent=0.3),
        effect.duration == 4,
        effect.delta == Stat(flat=5, percent=0.5),
        isclose(effect.accuracy, 0.6),
        effect.removable is False,
    ]

    assert_conditions(conditions)
