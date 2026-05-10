"""Tests for target processing's filter_monsters() method."""

from pytest import fixture
from src.base.monster import Monster
from tests.utils import assert_conditions
from src.processors.targets import filter_monsters


@fixture
def targets():
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

    return [
        monster_0,
        monster_1,
        monster_2,
        monster_3,
        monster_4,
    ]


def test_filter_lowest_hp_monsters(targets):
    filtered_monsters = filter_monsters(
        targets,
        k=1,
        method="FIRST",
        sort_function=(lambda x: x.hp),
    )
    
    conditions = [
        len(filtered_monsters) == 1,

        filtered_monsters[0].local_id == "MONSTER_0",
        filtered_monsters[0].hp == 0,
    ]
    
    assert_conditions(conditions)


def test_filter_highest_hp_monsters(targets):
    filtered_monsters = filter_monsters(
        targets,
        k=1,
        method="LAST",
        sort_function=(lambda x: x.hp),
    )
    
    conditions = [
        len(filtered_monsters) == 1,

        filtered_monsters[0].local_id == "MONSTER_4",
        filtered_monsters[0].hp == 200,
    ]
    
    assert_conditions(conditions)


def test_filter_alive_monsters(targets):
    filtered_monsters = filter_monsters(
        targets,
        k=2,
        method="FIRST",
        sort_function=(lambda x: x.hp),
        alive=True,
    )
    
    conditions = [
        len(filtered_monsters) == 2,

        filtered_monsters[0].local_id == "MONSTER_1",
        filtered_monsters[0].hp == 1,

        filtered_monsters[1].local_id == "MONSTER_2",
        filtered_monsters[1].hp == 10,
    ]
    
    assert_conditions(conditions)


def test_filter_hurt_monsters(targets):
    filtered_monsters = filter_monsters(
        targets,
        k=2,
        method="LAST",
        sort_function=(lambda x: x.hp),
        hurt=True,
    )
    
    conditions = [
        len(filtered_monsters) == 2,

        filtered_monsters[0].local_id == "MONSTER_3",
        filtered_monsters[0].hp == 100,

        filtered_monsters[1].local_id == "MONSTER_2",
        filtered_monsters[1].hp == 10,
    ]
    
    assert_conditions(conditions)
