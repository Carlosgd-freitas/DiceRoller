"""Tests for Logger class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.locales.languages import Language
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.logger.logger import Logger


def test_logger_change_language(loggers: Dict):
    logger: Logger = loggers["logger"]

    logger.change_language(Language.PT_BR)

    conditions = [
        logger.language == Language.PT_BR,
        len(logger._messages.keys()) > 0,
    ]

    assert_conditions(conditions)


def test_logger_get_namespace(loggers: Dict):
    logger: Logger = loggers["logger"]

    namespace = logger.get_namespace(namespace="base")

    conditions = [
        isinstance(namespace, Dict),
        len(namespace.keys()) > 0,
        all([isinstance(value, dict) for _, value in namespace.items()]),
    ]

    assert_conditions(conditions)


def test_logger_get_message_group(loggers: Dict):
    logger: Logger = loggers["logger"]

    message_group = logger.get_message_group(
        namespace="base", message_group="ATTRIBUTES"
    )

    conditions = [
        isinstance(message_group, Dict),
        len(message_group.keys()) > 0,
        all([isinstance(value, str) for _, value in message_group.items()]),
    ]

    assert_conditions(conditions)


def test_logger_get_message(loggers: Dict):
    logger: Logger = loggers["logger"]

    message = logger.get_message(namespace="base", message_group="ATTRIBUTES", key="hp")

    conditions = [
        isinstance(message, str),
        "hp" in message.lower(),
    ]

    assert_conditions(conditions)


def test_logger_get_colored_message(loggers: Dict):
    logger: Logger = loggers["logger"]

    keyword = Keyword.BURN

    message = logger.get_colored_message(
        keyword=keyword,
        namespace="effects",
        message_group=keyword.name,
        key="name",
    )

    conditions = [
        isinstance(message, str),
        "burn" in message.lower(),
    ]

    assert_conditions(conditions)


def test_logger_pluralize(loggers: Dict):
    logger: Logger = loggers["logger"]

    message = logger.pluralize(
        1,
        namespace="base",
        message_group="LEXICON",
        key="item",
    )

    conditions = [
        message == "item",
    ]

    message = logger.pluralize(
        2,
        namespace="base",
        message_group="LEXICON",
        key="item",
    )

    conditions.extend(
        [
            message == "items",
        ]
    )

    message = logger.pluralize(
        1,
        namespace="base",
        message_group="LEXICON",
        key="items",
    )

    conditions.extend(
        [
            message == "item",
        ]
    )

    message = logger.pluralize(
        2,
        namespace="base",
        message_group="LEXICON",
        key="items",
    )

    conditions.extend(
        [
            message == "items",
        ]
    )

    assert_conditions(conditions)
