"""Tests for target selecting methods."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.effect import EffectType
from src.base.monster import LifeState, Monster
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.stun import StunEffect
from src.systems.targeting.selectors.random_selector import RandomSelector
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.systems.targeting.selectors.manager import SelectorManager


def test_get_targets(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector_manager: SelectorManager = combat["selector_manager"]

    side = Side(effects=[AttackEffect(1)])

    targets = selector_manager.get_targets(
        side,
        monsters[0],
        allies=monsters[1:3],
        enemies=monsters[3:],
        k=1,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id
        in ["MONSTER_0", "MONSTER_1", "MONSTER_2", "MONSTER_3", "MONSTER_4"],
    ]

    assert_conditions(conditions)


def test_get_targets_random(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_random(
        monsters,
        k=1,
        life_state=LifeState.ANY,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id
        in ["MONSTER_0", "MONSTER_1", "MONSTER_2", "MONSTER_3", "MONSTER_4"],
    ]

    assert_conditions(conditions)


def test_get_targets_lowest_hp(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_lowest_hp(
        monsters,
        k=1,
        life_state=LifeState.ALIVE,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_get_targets_highest_hp(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_highest_hp(
        monsters,
        k=1,
        life_state=LifeState.ALIVE,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_targets_lowest_max_hp(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_lowest_max_hp(
        monsters,
        k=1,
        life_state=LifeState.ANY,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_get_targets_highest_max_hp(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    targets = selector._get_targets_highest_max_hp(
        monsters,
        k=1,
        life_state=LifeState.ANY,
    )

    conditions = [
        len(targets) == 1,
        targets[0].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_get_targets_most_effects(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    for i in range(5):
        monsters[i].effects = [StunEffect() for _ in range(i)]

    targets = selector._get_targets_most_effects(
        monsters,
        effect_type=EffectType.DEBUFF,
        k=2,
        life_state=LifeState.ANY,
    )

    conditions = [
        len(targets) == 2,
        targets[0].local_id == "MONSTER_4",
        targets[1].local_id == "MONSTER_3",
    ]

    assert_conditions(conditions)


def test_get_targets_least_effects(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = RandomSelector()

    for i in range(5):
        monsters[i].effects = [StunEffect() for _ in range(i)]

    targets = selector._get_targets_least_effects(
        monsters,
        effect_type=EffectType.DEBUFF,
        k=2,
        life_state=LifeState.ANY,
    )

    conditions = [
        len(targets) == 2,
        targets[0].local_id == "MONSTER_0",
        targets[1].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)
