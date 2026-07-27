"""Tests for Effect class."""

from src.base.life_state import LifeState
from src.effects.attack import AttackEffect
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
