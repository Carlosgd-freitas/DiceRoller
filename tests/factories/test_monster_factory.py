"""Tests for MonsterFactory class."""

from __future__ import annotations

from src.factories.monster import MonsterFactory
from src.monsters.slime import Slime
from tests.utils import assert_conditions


def test_create_monster_simple():
    monster = MonsterFactory.create_monster("SLIME")

    conditions = [
        isinstance(monster, Slime),
        monster.global_id == "SLIME",
    ]

    assert_conditions(conditions)


def test_create_monster_args():
    monster = MonsterFactory.create_monster(
        "SLIME",
        local_id="SLIME_0",
    )

    conditions = [
        isinstance(monster, Slime),
        monster.global_id == "SLIME",
        monster.local_id == "SLIME_0",
    ]

    assert_conditions(conditions)
