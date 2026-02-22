"""Tests for restoration effects processing."""

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
        mana=0,
    )
    monster_1 = Monster(
        local_id="MONSTER_1",
        hp=5,
        max_hp=10,
        mana=0,
    )

    return [
        monster_0,
        monster_1,
    ]


def test_keyword_heal(monsters):
    side = Side(
        effects=[
            Effect(Keyword.HEAL, 6),
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
        monsters[0].hp == 10,
        monsters[0].max_hp == 10,
    ]

    assert all(conditions)


def test_keyword_mana(monsters):
    side = Side(
        effects=[
            Effect(Keyword.MANA, 2),
        ]
    )

    mana_before = monsters[0].mana

    targets = process_effect(
        side.effects[0],
        source=monsters[1],
        targets=[monsters[0]],
    )
    
    conditions = [
        len(targets) == 1,

        monsters[0].local_id == "MONSTER_0",
        mana_before == 0,
        monsters[0].mana == 2,
    ]

    assert all(conditions)
