"""Tests for Manager class."""

from typing import Dict

from src.locales.languages import Language
from src.systems.manager import Manager
from tests.utils import assert_conditions


def test_manager_change_language(managers: Dict):
    manager: Manager = managers["manager"]

    conditions = [
        manager.logger.language == Language.EN_US,
    ]

    manager.change_language(Language.PT_BR)

    conditions.extend(
        [
            manager.logger.language == Language.PT_BR,
            len(manager.logger._messages.keys()) > 0,
        ]
    )

    assert_conditions(conditions)


def test_manager_toggle_logging(managers: Dict):
    manager: Manager = managers["manager"]

    conditions = [
        manager.logger.enabled is False,
    ]

    manager.toggle_logging(True)

    conditions.extend(
        [
            manager.logger.enabled is True,
        ]
    )

    assert_conditions(conditions)
