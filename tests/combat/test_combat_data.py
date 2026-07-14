"""Tests for CombatData."""

from copy import deepcopy

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.base.team import Team
from src.combat.manager import CombatData, are_combat_data_equivalent
from src.effects.attack import AttackEffect
from tests.utils import assert_conditions


def test_combat_data_is_equivalent():
    effect_0 = AttackEffect()
    effect_1 = AttackEffect(
        value=10,
        value_percent=11,
        duration=12,
        decay=13,
        accuracy=0.14,
        removable=False,
        target_keywords=[Keyword.BURN],
    )

    side_0 = Side(effects=[effect_0])
    side_1 = Side(effects=[effect_1])

    dice_0 = Dice(sides=[side_0])
    dice_1 = Dice(sides=[side_1])

    monster_0 = Monster(
        global_id="ID_0",
        hp=1,
        max_hp=2,
        dice=[dice_0],
    )

    monster_1 = Monster(
        global_id="ID_1",
        hp=1,
        max_hp=2,
        dice=[dice_1],
    )

    team_0 = Team(
        members=[monster_0],
    )

    team_1 = Team(
        members=[monster_1],
    )

    combat_data_0: CombatData = {"teams": [deepcopy(team_0)]}

    combat_data_1: CombatData = {"teams": [deepcopy(team_0)]}

    combat_data_2: CombatData = {"teams": [deepcopy(team_1)]}

    conditions = [
        are_combat_data_equivalent(combat_data_0, combat_data_0) is True,
        are_combat_data_equivalent(combat_data_0, combat_data_1) is True,
        are_combat_data_equivalent(combat_data_0, combat_data_2) is False,
    ]

    assert_conditions(conditions)
