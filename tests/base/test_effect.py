"""Tests for Effect class."""

from src.base.effect import get_effect_summary
from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.base.stat import Stat
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.nothing import NothingEffect
from tests.utils import assert_conditions


def test_effect_get_requirements():
    effect = NothingEffect()

    requirements = effect.get_requirements()

    conditions = [
        isinstance(requirements["source_life_state"], LifeState),
        isinstance(requirements["target_life_state"], LifeState),
    ]

    assert_conditions(conditions)


def test_effect_is_equivalent():
    effect_0 = NothingEffect()
    effect_1 = NothingEffect()
    effect_2 = AttackEffect()

    conditions = [
        effect_0.is_equivalent(effect_0) is True,
        effect_0.is_equivalent(effect_1) is True,
        effect_0.is_equivalent(effect_2) is False,
    ]

    assert_conditions(conditions)


def test_get_effect_summary():
    effects = [
        AttackEffect(Stat(flat=1)),
        BlockEffect(Stat(flat=2)),
        AbsorbEffect(Stat(flat=3)),
    ]

    effect_summary = get_effect_summary(effects)

    conditions = [
        len(effect_summary) == 2,
        "OFFENSIVE" in effect_summary.keys(),
        effect_summary["OFFENSIVE"] == [Keyword.ATTACK],
        "DEFENSIVE" in effect_summary.keys(),
        effect_summary["DEFENSIVE"] == [Keyword.BLOCK, Keyword.ABSORB],
    ]

    assert_conditions(conditions)
