"""Tests for Menu class."""

from typing import Dict

from src.locales.languages import Language
from src.menus.menu import Menu
from src.menus.option import Option
from tests.utils import assert_conditions


def test_menu_change_language(menus: Dict):
    menu: Menu = menus["main_menu"]

    conditions = [
        menu.logger.language == Language.EN_US,
    ]

    menu.change_language(Language.PT_BR)

    conditions.extend(
        [
            menu.logger.language == Language.PT_BR,
            len(menu.logger._messages.keys()) > 0,
        ]
    )

    assert_conditions(conditions)


def test_menu_exit_options(menus: Dict):
    menu: Menu = menus["main_menu"]

    option_0 = Option(
        id="EXIT",
        key="0",
        message="",
    )

    try:
        menu.process_option(option_0)
        suceeded = True
    except Exception:
        suceeded = False

    conditions = [
        suceeded is True,
    ]

    option_1 = Option(
        id="RETURN",
        key="1",
        message="",
    )

    try:
        menu.process_option(option_1)
        suceeded = True
    except Exception:
        suceeded = False

    conditions.extend(
        [
            suceeded is True,
        ]
    )

    assert_conditions(conditions)
