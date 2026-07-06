"""Tests for Compendium class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.compendium.compendium import CompendiumLevel
from src.locales.languages import Language
from src.menus.option import Option
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.compendium.compendium import Compendium


def test_compendium_change_language(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    compendium.change_language(Language.PT_BR)

    conditions = [
        compendium.logger.language == Language.PT_BR,
        len(compendium.logger._messages.keys()) > 0,
    ]

    assert_conditions(conditions)


def test_compendium_previous_page(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    option = Option(
        id="PREVIOUS_PAGE",
        key="0",
        message="",
    )

    compendium.page_number = 1
    compendium.process_option(option)

    conditions = [
        compendium.page_number == 1,
    ]

    compendium.page_number = 3
    compendium.process_option(option)

    conditions.extend(
        [
            compendium.page_number == 2,
        ]
    )

    assert_conditions(conditions)


def test_compendium_next_page(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    option = Option(
        id="NEXT_PAGE",
        key="0",
        message="",
    )

    compendium.page_number = 1
    compendium.process_option(option)

    conditions = [
        compendium.page_number == 2,
    ]

    compendium.page_number = compendium.num_pages
    compendium.process_option(option)

    conditions.extend(
        [
            compendium.page_number == compendium.num_pages,
        ]
    )

    assert_conditions(conditions)


def test_compendium_previous_item(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    option = Option(
        id="PREVIOUS_ITEM",
        key="0",
        message="",
    )

    compendium.item_number = 1
    compendium.process_option(option)

    conditions = [
        compendium.item_number == 1,
    ]

    compendium.item_number = 3
    compendium.process_option(option)

    conditions.extend(
        [
            compendium.item_number == 2,
        ]
    )

    assert_conditions(conditions)


def test_compendium_next_item(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    option = Option(
        id="NEXT_ITEM",
        key="0",
        message="",
    )

    compendium.item_number = 1
    compendium.process_option(option)

    conditions = [
        compendium.item_number == 2,
    ]

    compendium.item_number = len(compendium.items)
    compendium.process_option(option)

    conditions.extend(
        [
            compendium.item_number == len(compendium.items),
        ]
    )

    assert_conditions(conditions)


def test_compendium_exit_options(compendiums: Dict):
    compendium: Compendium = compendiums["effect_compendium"]

    option_0 = Option(
        id="RETURN",
        key="0",
        message="",
    )

    option_1 = Option(
        id="EXIT",
        key="1",
        message="",
    )

    conditions = [
        compendium.level == CompendiumLevel.PAGE,
    ]

    compendium.process_option(option_0)

    conditions.extend(
        [
            compendium.level == CompendiumLevel.PAGE,
        ]
    )

    compendium.process_option(option_1)

    conditions.extend(
        [
            compendium.level == CompendiumLevel.PAGE,
        ]
    )

    assert_conditions(conditions)
