"""Tests for offensive effects processing."""

from pytest import fixture
from src.base.side import Side
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword
from src.processors.effects import process_effect


@fixture
def monsters():
    monster_0 = Monster(
        local_id="MONSTER_0",
        hp=5,
        max_hp=10,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=5,
        max_hp=10,
    )

    return [
        monster_0,
        monster_1,
    ]


def test_keyword_attack(monsters):
    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        source=monsters[1],
        targets=[monsters[0]],
    )

    conditions = [
        len(targets) == 1,

        monsters[0].local_id == "MONSTER_0",
        monsters[0].hp == 0,
        monsters[0].max_hp == 10,
    ]

    assert all(conditions)


def test_keyword_curse(monsters):
    side = Side(
        effects=[
            Effect(Keyword.CURSE, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        source=monsters[0],
        targets=[monsters[0]],
    )

    conditions = [
        len(targets) == 1,

        monsters[0].local_id == "MONSTER_0",
        monsters[0].hp == 0,
        monsters[0].max_hp == 10,
    ]

    assert all(conditions)
