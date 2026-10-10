"""Tests for MonsterFactory class."""

from __future__ import annotations

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
