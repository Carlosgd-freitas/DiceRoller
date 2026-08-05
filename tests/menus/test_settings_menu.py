"""Tests for SettingsMenu class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.locales.languages import Language
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.menus.option import Option
    from src.menus.settings_menu import SettingsMenu


def test_menu_settings_language_option(menus: Dict):
    settings_menu: SettingsMenu = menus["settings_menu"]
    languge_option: Option = None

    for option in settings_menu.options:
        if option.id == "LANGUAGE":
            languge_option = option
            break

    conditions = [
        settings_menu.settings.language == Language.EN_US,
    ]

    settings_menu.process_option(languge_option)

    conditions.extend(
        [
            settings_menu.settings.language == Language.PT_BR,
        ]
    )

    settings_menu.process_option(languge_option)

    conditions.extend(
        [
            settings_menu.settings.language == Language.EN_US,
        ]
    )

    assert_conditions(conditions)


def test_menu_settings_monster_end_turn_option(menus: Dict):
    settings_menu: SettingsMenu = menus["settings_menu"]
    monster_end_turn_option: Option = None

    for option in settings_menu.options:
        if option.id == "MONSTER_END_TURN":
            monster_end_turn_option = option
            break

    conditions = [
        settings_menu.settings.monster_end_turn == "MANUAL",
    ]

    settings_menu.process_option(monster_end_turn_option)

    conditions.extend(
        [
            settings_menu.settings.monster_end_turn == "AUTO",
        ]
    )

    settings_menu.process_option(monster_end_turn_option)

    conditions.extend(
        [
            settings_menu.settings.monster_end_turn == "MANUAL",
        ]
    )

    assert_conditions(conditions)
