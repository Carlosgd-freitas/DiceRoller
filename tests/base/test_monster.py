"""Tests for Monster class."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.effects.attack import AttackEffect
from tests.utils import assert_conditions


def test_monster_is_equivalent():
    effect = AttackEffect(Stat(flat=1))
    side = Side(effects=[effect])
    dice = Dice(sides=[side])

    monster_0 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    monster_1 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    monster_2 = Monster(
        global_id="ID_1",
        hp=1,
        max_hp=2,
        dice=[deepcopy(dice)],
    )

    conditions = [
        monster_0.is_equivalent(monster_0) is True,
        monster_0.is_equivalent(monster_1) is True,
        monster_0.is_equivalent(monster_2) is False,
    ]

    assert_conditions(conditions)
