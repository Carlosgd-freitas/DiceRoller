"""Tests for target selecting methods."""

from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.stun import StunEffect
from src.targeting.selectors.random_selector import RandomSelector
from tests.utils import assert_conditions


def test_get_targets_random(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = RandomSelector()

    targets = selector._get_targets_random(
        combat_manager.order,
        k=1,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id
        in ["MONSTER_0", "MONSTER_1", "MONSTER_2", "MONSTER_3", "MONSTER_4"],
    ]

    assert_conditions(conditions)


def test_get_targets_lowest_hp(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = RandomSelector()

    targets = selector._get_targets_lowest_hp(
        combat_manager.order,
        k=1,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_get_targets_highest_hp(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = RandomSelector()

    targets = selector._get_targets_highest_hp(
        combat_manager.order,
        k=1,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_targets_with_effects(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = RandomSelector()
    effect = StunEffect()

    combat_manager.order[0].apply_effect(effect)
    combat_manager.order[1].apply_effect(effect)

    targets = selector._get_targets_with_effects(
        combat_manager.order, k=2, effects=[Keyword.STUN]
    )

    targets_ids = set([target.local_id for target in targets])

    conditions = [
        len(targets) == 2,
        targets_ids == {"MONSTER_1", "MONSTER_2"},
    ]

    assert_conditions(conditions)


def test_get_targets_without_effects(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = RandomSelector()
    effect = StunEffect()

    combat_manager.order[0].apply_effect(effect)
    combat_manager.order[1].apply_effect(effect)

    targets = selector._get_targets_without_effects(
        combat_manager.order, k=2, effects=[Keyword.STUN]
    )

    targets_ids = set([target.local_id for target in targets])

    conditions = [
        len(targets) == 2,
        targets_ids == {"MONSTER_3", "MONSTER_4"},
    ]

    assert_conditions(conditions)
