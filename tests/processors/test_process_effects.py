"""Tests for effect processing's process_effect() method."""

from pytest import fixture
from src.base.side import Side
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword
from src.processors.effects import process_effect


@fixture
def targets():
    monster = Monster(
        local_id="MONSTER",
        hp=5,
        max_hp=10,
    )

    return [monster]


def test_attack_keyword(targets):
    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        targets,
    )
    
    conditions = [
        len(targets) == 1,

        targets[0].local_id == "MONSTER",
        targets[0].hp == 0,
        targets[0].max_hp == 10,
    ]
    
    assert all(conditions)


def test_heal_keyword(targets):
    side = Side(
        effects=[
            Effect(Keyword.HEAL, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        targets,
    )
    
    conditions = [
        len(targets) == 1,

        targets[0].local_id == "MONSTER",
        targets[0].hp == 10,
        targets[0].max_hp == 10,
    ]
    
    assert all(conditions)
