"""Tests for target filtering methods."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.keywords import Keyword
from src.effects.burn import BurnEffect
from src.effects.stun import StunEffect
from src.targeting.filters import filter_entities
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster


def test_filter_method_first(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=1,
        method="FIRST",
        life_state="ANY",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_filter_method_last(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=3,
        method="LAST",
        life_state="ANY",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_4",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_filter_life_state_alive(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=2,
        method="FIRST",
        life_state="ALIVE",
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_1",
        filtered[0].hp == 1,
        filtered[1].local_id == "MONSTER_2",
        filtered[1].hp == 10,
    ]

    assert_conditions(conditions)


def test_filter_life_state_dead(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=2,
        method="FIRST",
        life_state="DEAD",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
        filtered[0].hp == 0,
    ]

    assert_conditions(conditions)


def test_filter_hurt(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=2,
        method="LAST",
        life_state="ANY",
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


def test_filter_sort_functions_single(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    filtered = filter_entities(
        monsters,
        k=1,
        method="FIRST",
        sort_functions=[lambda x: x.hp],
        life_state="ALIVE",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_1",
        filtered[0].hp == 1,
    ]

    assert_conditions(conditions)


def test_filter_sort_functions_multiple(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    for monster in monsters:
        monster.mana = 5

    filtered = filter_entities(
        monsters,
        k=1,
        method="FIRST",
        sort_functions=[lambda x: x.mana, lambda x: -x.hp],
        life_state="ANY",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_4",
        filtered[0].hp == 200,
        filtered[0].mana == 5,
    ]

    assert_conditions(conditions)


def test_filter_keyword_whitelist(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    monsters[0].apply_effect(effect_burn)
    monsters[1].apply_effect(effect_stun)

    filtered = filter_entities(
        monsters,
        k=2,
        method="FIRST",
        life_state="ANY",
        keyword_whitelist=[Keyword.BURN],
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_filter_keyword_blacklist(managers: Dict):
    monsters: List[Monster] = managers["monsters"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    monsters[0].apply_effect(effect_burn)
    monsters[1].apply_effect(effect_stun)

    filtered = filter_entities(
        monsters,
        k=10,
        method="FIRST",
        life_state="ANY",
        keyword_blacklist=[Keyword.STUN],
    )

    conditions = [
        len(filtered) == 4,
        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_2",
        filtered[2].local_id == "MONSTER_3",
        filtered[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)
