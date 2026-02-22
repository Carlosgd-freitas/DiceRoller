"""Tests for debuff effects processing."""

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


def test_keyword_blind(monsters):
    side_0 = Side(
        effects=[
            Effect(
                Keyword.BLIND,
                value=1,
                duration=1,
            ),
        ]
    )
    side_1 = Side(
        effects=[
            Effect(Keyword.HEAL, 2),
        ]
    )

    _ = process_effect(
        side_0.effects[0],
        source=monsters[1],
        targets=[monsters[0]],
    )

    _ = process_effect(
        side_1.effects[0],
        source=monsters[0],
        targets=[monsters[0]],
    )

    _ = process_effect(
        side_1.effects[0],
        source=monsters[0],
        targets=[monsters[1]],
    )

    conditions = [
        monsters[0].local_id == "MONSTER_0",
        len(monsters[0].effects) == 1,
        monsters[0].get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
        monsters[0].get_effect(Keyword.BLIND).value == 1,
        monsters[0].hp == 7,

        monsters[1].local_id == "MONSTER_1",
        len(monsters[1].effects) == 0,
        monsters[1].get_effect(Keyword.BLIND) == None,
        monsters[1].hp == 5,
    ]

    assert all(conditions)
