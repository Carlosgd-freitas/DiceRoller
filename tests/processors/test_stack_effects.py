"""Tests for stacking effects."""

from math import isclose
from src.base.effect import Effect
from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.processors.effects import stack_effect


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
    
    monster = stack_effect(
        effect=effect,
        target=monster,
    )

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    assert all([
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 1,
        stacked_effect.duration == 2,
        stacked_effect.decay == 3,
        isclose(stacked_effect.accuracy, 0.1),
    ])


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

    monster.effects.append(effect_0)
    
    monster = stack_effect(
        effect=effect_1,
        target=monster,
        rules=[
            ("add", "value"),
            ("add", "duration"),
            ("add", "decay"),
            ("add", "accuracy"),
        ],
    )

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    assert all([
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 5,
        stacked_effect.duration == 7,
        stacked_effect.decay == 9,
        isclose(stacked_effect.accuracy, 0.3),
    ])


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

    monster.effects.append(effect_0)
    
    monster = stack_effect(
        effect=effect_1,
        target=monster,
        rules=[
            ("overwrite", "value"),
            ("overwrite", "duration"),
            ("overwrite", "decay"),
            ("overwrite", "accuracy"),
        ],
    )

    stacked_effect = monster.get_effect(Keyword.NOTHING)

    assert all([
        stacked_effect is not None,
        len(monster.effects) == 1,

        stacked_effect.keyword == Keyword.NOTHING,
        stacked_effect.value == 4,
        stacked_effect.duration == 5,
        stacked_effect.decay == 6,
        isclose(stacked_effect.accuracy, 0.2),
    ])


def test_stack_effect_remove(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]
    monster = combat_manager.order[0]

    effect_0 = Effect(
        Keyword.WEAKEN,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_1 = Effect(
        Keyword.FORTIFY,
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_2 = Effect(
        Keyword.STRENGTHEN,
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.effects.extend([effect_0, effect_1])
    
    monster = stack_effect(
        effect=effect_2,
        target=monster,
        remove=[
            Keyword.WEAKEN,
        ]
    )

    assert all([
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
    ])
