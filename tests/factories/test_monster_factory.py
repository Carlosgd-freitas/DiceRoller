"""Tests for MonsterFactory class."""

from __future__ import annotations

from src.base.monster import Monster
from src.factories.monster import MonsterFactory
from src.monsters.slime import Slime
from tests.utils import assert_conditions


def test_monster_factory_create_simple():
    monster = MonsterFactory.create("SLIME")

    conditions = [
        isinstance(monster, Slime),
        monster.global_id == "SLIME",
    ]

    assert_conditions(conditions)


def test_monster_factory_create_args():
    monster = MonsterFactory.create(
        "SLIME",
        local_id="SLIME_0",
    )

    conditions = [
        isinstance(monster, Slime),
        monster.global_id == "SLIME",
        monster.local_id == "SLIME_0",
    ]

    assert_conditions(conditions)


def test_monster_factory_get_all_objects():
    all_monsters = MonsterFactory.get_all_objects()

    conditions = [
        isinstance(all_monsters, list),
        len(all_monsters) > 0,
        all([isinstance(monster, Monster) for monster in all_monsters]),
    ]

    assert_conditions(conditions)
