"""Tests for loggers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.locales.languages import Language
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.logger.logger import Logger


def test_change_language(loggers: Dict):
    logger: Logger = loggers["logger"]

    logger.change_language(Language.PT_BR)

    conditions = [
        logger.language == Language.PT_BR,
        len(logger._messages.keys()) > 0,
    ]

    assert_conditions(conditions)


def test_get_message_group(loggers: Dict):
    logger: Logger = loggers["logger"]

    message_group = logger.get_message_group(
        namespace="base", message_group="ATTRIBUTES"
    )

    conditions = [
        isinstance(message_group, Dict),
        len(message_group.keys()) > 0,
    ]

    assert_conditions(conditions)


def test_get_message(loggers: Dict):
    logger: Logger = loggers["logger"]

    message = logger.get_message(namespace="base", message_group="ATTRIBUTES", key="hp")

    conditions = [
        isinstance(message, str),
        "hp" in message.lower(),
    ]

    assert_conditions(conditions)


def test_get_colored_message(loggers: Dict):
    logger: Logger = loggers["logger"]

    message = logger.get_colored_message(
        namespace="effects",
        message_group="KEYWORDS",
        keyword=Keyword.BURN,
    )

    conditions = [
        isinstance(message, str),
        "burn" in message.lower(),
    ]

    assert_conditions(conditions)
