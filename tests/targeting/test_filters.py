"""Tests for targe filtering methods."""

from pytest import fixture
from src.base.monster import Monster
from src.base.keywords import Keyword
from src.effects.burn import BurnEffect
from src.effects.stun import StunEffect
from src.targeting.filters import filter
from tests.utils import assert_conditions
from src.combat.manager import CombatManager


@fixture
def combat_manager():
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=0,
        max_hp=200,
    )

    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=1,
        max_hp=200,
    )

    monster_2 = Monster(
        local_id="MONSTER_2",
        hp=10,
        max_hp=200,
    )

    monster_3 = Monster(
        local_id="MONSTER_3",
        hp=100,
        max_hp=200,
    )

    monster_4 = Monster(
        local_id="MONSTER_4",
        hp=200,
        max_hp=200,
    )

    combat_manager = CombatManager(
        teams=[
            [monster_0, monster_1, monster_2],
            [monster_3, monster_4],
        ],
        order_strategy="SET",
    )

    return combat_manager


def test_filter_first(combat_manager: CombatManager):
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


def test_filter_last(combat_manager: CombatManager):
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



def test_filter_alive(combat_manager: CombatManager):
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


def test_filter_hurt(combat_manager: CombatManager):
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


def test_filter_lowest_hp(combat_manager: CombatManager):
    filtered = filter(
        combat_manager.order,
        k=1,
        method="FIRST",
        sort_function=(lambda x: x.hp),
        alive=False,
    )

    conditions = [
        len(filtered) == 1,

        filtered[0].local_id == "MONSTER_0",
        filtered[0].hp == 0,
    ]

    assert_conditions(conditions)


def test_filter_highest_hp(combat_manager: CombatManager):
    filtered = filter(
        combat_manager.order,
        k=1,
        method="LAST",
        sort_function=(lambda x: x.hp),
        alive=False,
    )

    conditions = [
        len(filtered) == 1,

        filtered[0].local_id == "MONSTER_4",
        filtered[0].hp == 200,
    ]

    assert_conditions(conditions)


def test_filter_with_effect(combat_manager: CombatManager):
    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    combat_manager.order[1].apply_effect(effect_burn)
    combat_manager.order[2].apply_effect(effect_stun)

    filtered = filter(
        combat_manager.order,
        k=2,
        method="FIRST",
        alive=False,
        keyword_whitelist=[Keyword.BURN]
    )

    conditions = [
        len(filtered) == 1,

        filtered[0].local_id == "MONSTER_1",
    ]

    assert_conditions(conditions)


def test_filter_without_effect(combat_manager: CombatManager):
    effect_burn = BurnEffect()
    effect_stun = StunEffect()

    combat_manager.order[1].apply_effect(effect_burn)
    combat_manager.order[2].apply_effect(effect_stun)

    filtered = filter(
        combat_manager.order,
        k=10,
        method="FIRST",
        alive=False,
        keyword_blacklist=[Keyword.STUN]
    )

    conditions = [
        len(filtered) == 4,

        filtered[0].local_id == "MONSTER_0",
        filtered[1].local_id == "MONSTER_1",
        filtered[2].local_id == "MONSTER_3",
        filtered[3].local_id == "MONSTER_4",
    ]

    assert_conditions(conditions)
