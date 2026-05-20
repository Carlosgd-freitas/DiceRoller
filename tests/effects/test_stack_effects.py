"""Tests for stacking effects."""

from math import isclose
from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.burn import BurnEffect
from src.effects.freeze import FreezeEffect
from src.effects.nothing import NothingEffect
from src.effects.stun import StunEffect
from tests.utils import assert_conditions


def test_stack_effect_new(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster = combat_manager.order[1]

    effect = NothingEffect(
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )

    monster.apply_effect(effect)

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


def test_stack_effect_add(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster = combat_manager.order[1]

    effect_0 = NothingEffect(
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_1 = NothingEffect(
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.apply_effect(effect_0)

    monster.apply_effect(
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


def test_stack_effect_overwrite(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster = combat_manager.order[1]

    effect_0 = NothingEffect(
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_1 = NothingEffect(
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.apply_effect(effect_0)

    monster.apply_effect(
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


def test_stack_effect_remove(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster = combat_manager.order[1]

    effect_freeze = FreezeEffect(
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_stun = StunEffect(
        value=1,
        duration=2,
        decay=3,
        accuracy=0.1,
    )
    effect_burn = BurnEffect(
        value=4,
        duration=5,
        decay=6,
        accuracy=0.2,
    )

    monster.apply_effect(effect_freeze)
    monster.apply_effect(effect_stun)
    monster.apply_effect(effect_burn)

    conditions = [
        len(monster.effects) == 2,
        monster.get_effect(Keyword.STUN).keyword == Keyword.STUN,
        monster.get_effect(Keyword.STUN).value == 1,
        monster.get_effect(Keyword.STUN).duration == 2,
        monster.get_effect(Keyword.STUN).decay == 3,
        isclose(monster.get_effect(Keyword.STUN).accuracy, 0.1),
        monster.get_effect(Keyword.BURN).keyword == Keyword.BURN,
        monster.get_effect(Keyword.BURN).value == 4,
        monster.get_effect(Keyword.BURN).duration == 5,
        monster.get_effect(Keyword.BURN).decay == 6,
        isclose(monster.get_effect(Keyword.BURN).accuracy, 0.2),
        monster.get_effect(Keyword.FREEZE) is None,
    ]

    assert_conditions(conditions)
