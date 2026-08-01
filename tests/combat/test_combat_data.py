"""Tests for CombatData."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.team import Team
from src.combat.manager import (
    CombatData,
    are_combat_data_equivalent,
)
from src.combat.order_strategy import OrderStrategy
from src.effects.attack import AttackEffect
from tests.utils import assert_conditions


def test_combat_data_is_equivalent():
    effect = AttackEffect()
    side = Side(effects=[effect])
    dice = Dice(sides=[side])

    monster = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[dice],
    )

    team = Team(
        members=[monster],
    )

    combat_data_0: CombatData = {
        "order_strategy": OrderStrategy.FASTER,
        "teams": [deepcopy(team)],
    }

    combat_data_1: CombatData = {
        "order_strategy": OrderStrategy.FASTER,
        "teams": [deepcopy(team)],
    }

    combat_data_2: CombatData = {
        "order_strategy": OrderStrategy.SLOWER,
        "teams": [deepcopy(team), deepcopy(team)],
    }

    conditions = [
        are_combat_data_equivalent(combat_data_0, combat_data_0) is True,
        are_combat_data_equivalent(combat_data_0, combat_data_1) is True,
        are_combat_data_equivalent(combat_data_0, combat_data_2) is False,
    ]

    assert_conditions(conditions)
