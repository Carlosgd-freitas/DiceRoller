"""Tests for target filtering methods."""

from typing import Dict, List

from src.base.keywords import Keyword
from src.base.life_state import LifeState
from src.base.monster import Monster
from src.effects.burn import BurnEffect
from src.effects.immunity import ImmunityEffect
from src.effects.repel import RepelEffect
from src.effects.stun import StunEffect
from src.effects.taunt import TauntEffect
from src.systems.targeting.filters import filter_monsters
from tests.utils import assert_conditions


def test_filter_method_first(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=1,
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_filter_method_last(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=3,
        life_state=LifeState.ANY,
        method="LAST",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_4",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_2",
    ]

    assert_conditions(conditions)


def test_filter_life_state_alive(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=2,
        life_state=LifeState.ALIVE,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_1",
        filtered[0].hp == 1,
        filtered[1].local_id == "MONSTER_2",
        filtered[1].hp == 10,
    ]

    assert_conditions(conditions)


def test_filter_life_state_dead(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=2,
        life_state=LifeState.DEAD,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
        filtered[0].hp == 0,
    ]

    assert_conditions(conditions)


def test_filter_hurt(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=2,
        life_state=LifeState.ANY,
        hurt=True,
        method="LAST",
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_3",
        filtered[0].hp == 100,
        filtered[1].local_id == "MONSTER_2",
        filtered[1].hp == 10,
    ]

    assert_conditions(conditions)


def test_filter_sort_functions_single(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    filtered = filter_monsters(
        monsters,
        k=1,
        sort_functions=[lambda x: x.hp],
        life_state=LifeState.ALIVE,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_1",
        filtered[0].hp == 1,
    ]

    assert_conditions(conditions)


def test_filter_sort_functions_multiple(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    for monster in monsters:
        monster.mana = 5

    filtered = filter_monsters(
        monsters,
        k=1,
        sort_functions=[lambda x: x.mana, lambda x: -x.hp],
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_4",
        filtered[0].hp == 200,
        filtered[0].mana == 5,
    ]

    assert_conditions(conditions)


def test_filter_whitelist(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    whitelist = monsters[:2]

    filtered = filter_monsters(
        monsters,
        k=2,
        whitelist=whitelist,
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 2,
        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_filter_blacklist(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    blacklist = monsters[:2]

    filtered = filter_monsters(
        monsters,
        k=3,
        blacklist=blacklist,
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_2",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_filter_keyword_whitelist(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    monsters[0].apply_effect(effect_burn)
    monsters[1].apply_effect(effect_stun)

    filtered = filter_monsters(
        monsters,
        k=2,
        keyword_whitelist=[Keyword.BURN],
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)


def test_filter_keyword_blacklist(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    monsters[0].apply_effect(effect_burn)
    monsters[1].apply_effect(effect_stun)

    filtered = filter_monsters(
        monsters,
        k=10,
        keyword_blacklist=[Keyword.STUN],
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 4,
        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_2",
        filtered[2].local_id == "MONSTER_3",
        filtered[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_filter_ignore_immune_to(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    effect_immunity = ImmunityEffect(target_keywords=[Keyword.BURN])

    monsters[1].apply_effect(effect_immunity)
    monsters[2].apply_effect(effect_immunity)

    filtered = filter_monsters(
        monsters,
        k=10,
        ignore_immune_to=[Keyword.BURN],
        life_state=LifeState.ANY,
        method="FIRST",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_filter_consider_repel(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    monsters[0].apply_effect(RepelEffect())
    monsters[1].apply_effect(RepelEffect())

    filtered = filter_monsters(
        monsters,
        k=3,
        life_state=LifeState.ANY,
        consider=[Keyword.REPEL],
        method="FIRST",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_2",
        filtered[1].local_id == "MONSTER_3",
        filtered[2].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)


def test_filter_consider_taunt(combat: Dict):
    monsters: List[Monster] = combat["monsters"]

    monsters[3].apply_effect(TauntEffect())
    monsters[4].apply_effect(TauntEffect())

    filtered = filter_monsters(
        monsters,
        k=3,
        life_state=LifeState.ANY,
        consider=[Keyword.TAUNT],
        method="FIRST",
    )

    conditions = [
        len(filtered) == 3,
        filtered[0].local_id == "MONSTER_3",
        filtered[1].local_id == "MONSTER_4",
        filtered[2].local_id == "MONSTER_0",
    ]

    assert_conditions(conditions)
