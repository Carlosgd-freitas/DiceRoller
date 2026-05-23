"""Tests for target filtering methods."""

from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.burn import BurnEffect
from src.effects.stun import StunEffect
from src.targeting.filters import filter
from tests.utils import assert_conditions


def test_filter_first(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=1,
        method="FIRST",
        alive=False,
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_filter_last(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=3,
        method="LAST",
        alive=False,
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_4",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_filter_alive(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=2,
        method="FIRST",
        alive=True,
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_1",
        filtered[0].hp == 1,
        filtered[1].local_id == "MONSTER_2",
        filtered[1].hp == 10,
    ]

    assert_conditions(conditions)


def test_filter_hurt(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=2,
        method="LAST",
        alive=False,
        hurt=True,
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_3",
        filtered[0].hp == 100,
        filtered[1].local_id == "MONSTER_2",
        filtered[1].hp == 10,
    ]

    assert_conditions(conditions)


def test_filter_lowest_hp(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=1,
        method="FIRST",
        sort_functions=[lambda x: x.hp],
        alive=False,
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
        filtered[0].hp == 0,
    ]

    assert_conditions(conditions)


def test_filter_highest_hp(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    filtered = filter(
        combat_manager.order,
        k=1,
        method="LAST",
        sort_functions=[lambda x: x.hp],
        alive=False,
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_4",
        filtered[0].hp == 200,
    ]

    assert_conditions(conditions)


def test_filter_with_effect(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    combat_manager.order[1].apply_effect(effect_burn)
    combat_manager.order[2].apply_effect(effect_stun)

    filtered = filter(
        combat_manager.order,
        k=2,
        method="FIRST",
        alive=False,
        keyword_whitelist=[Keyword.BURN],
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_filter_without_effect(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    combat_manager.order[1].apply_effect(effect_burn)
    combat_manager.order[2].apply_effect(effect_stun)

    filtered = filter(
        combat_manager.order,
        k=10,
        method="FIRST",
        alive=False,
        keyword_blacklist=[Keyword.STUN],
    )

    conditions = [
        len(filtered) == 4,
        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_1",
        filtered[2].local_id == "MONSTER_3",
        filtered[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)
