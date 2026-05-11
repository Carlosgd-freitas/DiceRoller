"""Tests for stacking effects."""

from math import isclose
from src.base.effect import Effect
from src.base.keywords import Keyword
from tests.utils import assert_conditions
from src.combat.manager import CombatManager


def test_stack_effect_new(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]
    monster = combat_manager.order[0]

    effect = Effect(
        Keyword.NOTHING,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    
    monster.add_effect(effect)

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    conditions = [
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 1,
        stacked_effect.duration == 2,
        stacked_effect.decay == 3,
        isclose(stacked_effect.accuracy, 0.1),
    ]

    assert_conditions(conditions)


def test_stack_effect_add(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]
    monster = combat_manager.order[0]

    effect_0 = Effect(
        Keyword.NOTHING,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_1 = Effect(
        Keyword.NOTHING,
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.add_effect(effect_0)

    monster.add_effect(
        effect_1,
        stack_value="add",
        stack_duration="add",
        stack_decay="add",
        stack_accuracy="add",
    )

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    conditions = [
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 5,
        stacked_effect.duration == 7,
        stacked_effect.decay == 9,
        isclose(stacked_effect.accuracy, 0.3),
    ]

    assert_conditions(conditions)


def test_stack_effect_overwrite(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]
    monster = combat_manager.order[0]

    effect_0 = Effect(
        Keyword.NOTHING,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_1 = Effect(
        Keyword.NOTHING,
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.add_effect(effect_0)

    monster.add_effect(
        effect_1,
        stack_value="overwrite",
        stack_duration="overwrite",
        stack_decay="overwrite",
        stack_accuracy="overwrite",
    )

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    conditions = [
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 4,
        stacked_effect.duration == 5,
        stacked_effect.decay == 6,
        isclose(stacked_effect.accuracy, 0.2),
    ]

    assert_conditions(conditions)


def test_stack_effect_remove(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]
    monster = combat_manager.order[0]

    effect_weaken = Effect(
        Keyword.WEAKEN,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_fortify = Effect(
        Keyword.FORTIFY,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_strengthen = Effect(
        Keyword.STRENGTHEN,
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.add_effect(effect_weaken)
    monster.add_effect(effect_fortify)
    monster.add_effect(effect_strengthen)

    conditions = [
        len(monster.effects) == 2,

        monster.get_effect(Keyword.STRENGTHEN).keyword == Keyword.STRENGTHEN,
        monster.get_effect(Keyword.STRENGTHEN).value == 4,
        monster.get_effect(Keyword.STRENGTHEN).duration == 5,
        monster.get_effect(Keyword.STRENGTHEN).decay == 6,
        isclose(monster.get_effect(Keyword.STRENGTHEN).accuracy, 0.2),

        monster.get_effect(Keyword.FORTIFY).keyword == Keyword.FORTIFY,
        monster.get_effect(Keyword.FORTIFY).value == 1,
        monster.get_effect(Keyword.FORTIFY).duration == 2,
        monster.get_effect(Keyword.FORTIFY).decay == 3,
        isclose(monster.get_effect(Keyword.FORTIFY).accuracy, 0.1),

        monster.get_effect(Keyword.WEAKEN) == None,
    ]

    assert_conditions(conditions)
