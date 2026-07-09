"""Tests for CombatManager class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.locales.languages import Language
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.combat.manager import CombatData, CombatManager


def test_manager_change_language(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    conditions = [
        combat_manager.logger.language == Language.EN_US,
    ]

    combat_manager.change_language(Language.PT_BR)

    conditions.extend(
        [
            combat_manager.logger.language == Language.PT_BR,
            len(combat_manager.logger._messages.keys()) > 0,
            combat_manager.effect_manager.logger.language == Language.PT_BR,
            combat_manager.player_actions_menu.logger.language == Language.PT_BR,
        ]
    )

    assert_conditions(conditions)


def test_manager_toggle_logging(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    conditions = [
        combat_manager.logger.enabled is False,
    ]

    combat_manager.toggle_logging(True)

    conditions.extend(
        [
            combat_manager.logger.enabled is True,
            combat_manager.effect_manager.logger.enabled is True,
            combat_manager.player_actions_menu.logger.enabled is True,
        ]
    )

    assert_conditions(conditions)


def test_combat_manager_get_combat_data(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_data = combat_manager.get_combat_data()

    conditions = [
        combat_data["round"] == 1,
        combat_data["turn"] == 1,
        len(combat_data["teams"]) == 2,
    ]

    assert_conditions(conditions)


def test_combat_manager_set_combat_data(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_data: CombatData = {
        "round": 2,
        "turn": 3,
        "teams": [],
    }

    combat_manager.set_combat_data(combat_data)

    conditions = [
        combat_manager.round == 2,
        combat_manager.turn == 3,
        len(combat_manager.teams) == 0,
    ]

    assert_conditions(conditions)


def test_get_combat_status_winner(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for idx, team in enumerate(combat_manager.teams):
        for monster in team.members:
            if idx == 1:
                monster.hp = 0

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "WINNER",
        len(combat_status["ALIVE"]) == 1,
        len(combat_status["ALIVE"][0].members) == 3,
        len(combat_status["DEFEATED"]) == 1,
        len(combat_status["DEFEATED"][0].members) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_draw(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    for team in combat_manager.teams:
        for monster in team.members:
            monster.hp = 0

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "DRAW",
        len(combat_status["ALIVE"]) == 0,
        len(combat_status["DEFEATED"]) == 2,
        len(combat_status["DEFEATED"][0].members) == 3,
        len(combat_status["DEFEATED"][1].members) == 2,
    ]

    assert_conditions(conditions)


def test_get_combat_status_ongoing(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]

    combat_status = combat_manager.get_combat_status()

    conditions = [
        combat_status["status"] == "ONGOING",
        len(combat_status["ALIVE"]) == 2,
        len(combat_status["ALIVE"][0].members) == 3,
        len(combat_status["ALIVE"][1].members) == 2,
        len(combat_status["DEFEATED"]) == 0,
    ]

    assert_conditions(conditions)
