"""Tests for target selecting methods."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.keywords import Keyword
from src.effects.stun import StunEffect
from src.targeting.selectors.random_selector import RandomSelector
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster


def test_get_targets_random(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_random(
        monsters,
        k=1,
        life_state="ANY",
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id
        in ["MONSTER_0", "MONSTER_1", "MONSTER_2", "MONSTER_3", "MONSTER_4"],
    ]

    assert_conditions(conditions)


def test_get_targets_lowest_hp(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_lowest_hp(
        monsters,
        k=1,
        life_state="ALIVE",
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_get_targets_highest_hp(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_highest_hp(
        monsters,
        k=1,
        life_state="ALIVE",
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_targets_lowest_max_hp(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_lowest_max_hp(
        monsters,
        k=1,
        life_state="ANY",
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_get_targets_highest_max_hp(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_highest_max_hp(
        monsters,
        k=1,
        life_state="ANY",
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_targets_with_effects(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()
    effect = StunEffect()

    monsters[0].apply_effect(effect)
    monsters[1].apply_effect(effect)

    targets = selector._get_targets_with_effects(
        monsters,
        k=2,
        effects=[Keyword.STUN],
        life_state="ANY",
    )

    targets_ids = set([target.local_id for target in targets])

    conditions = [
        len(targets) == 2,
        targets_ids == {"MONSTER_0", "MONSTER_1"},
    ]

    assert_conditions(conditions)


def test_get_targets_without_effects(managers: Dict):
    monsters: List[Monster] = managers["monsters"]
    selector = RandomSelector()
    effect = StunEffect()

    monsters[0].apply_effect(effect)
    monsters[1].apply_effect(effect)

    targets = selector._get_targets_without_effects(
        monsters,
        k=3,
        effects=[Keyword.STUN],
        life_state="ANY",
    )

    targets_ids = set([target.local_id for target in targets])

    conditions = [
        len(targets) == 3,
        targets_ids == {"MONSTER_2", "MONSTER_3", "MONSTER_4"},
    ]

    assert_conditions(conditions)
