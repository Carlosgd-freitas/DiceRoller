"""Tests for locales modules."""

from typing import get_args

import pytest

from src.locales.languages import Language
from src.logger.logger import Logger, Namespace

PIVOT_LANGUAGE = Language.EN_US
ALL_CASES = [
    (language, namespace) for language in Language for namespace in get_args(Namespace)
]
TRANSLATED_CASES = [
    (language, namespace)
    for language, namespace in ALL_CASES
    if language != PIVOT_LANGUAGE
]


@pytest.fixture
def pivot() -> Logger:
    return Logger(
        enabled=False,
        language=PIVOT_LANGUAGE,
    )


def assert_namespace_exists(
    logger: Logger,
    namespace_name: Namespace,
):
    namespace = logger.get_namespace(
        namespace=namespace_name,
    )

    assert isinstance(namespace, dict), (
        f"Namespace existence test failed for '{logger.language.value}"
        f"/{namespace_name}'."
    )


@pytest.mark.parametrize(
    "language, namespace_name",
    ALL_CASES,
)
def test_namespaces_integrity(language, namespace_name):
    logger = Logger(enabled=False, language=language)

    assert_namespace_exists(
        logger,
        namespace_name,
    )


def assert_message_groups_exists(
    pivot: Logger,
    logger: Logger,
    namespace_name: Namespace,
):
    pivot_namespace = pivot.get_namespace(
        namespace=namespace_name,
    )
    logger_namespace = logger.get_namespace(
        namespace=namespace_name,
    )

    pivot_message_group_names = set(pivot_namespace.keys())
    logger_message_group_names = set(logger_namespace.keys())

    assert pivot_message_group_names == logger_message_group_names, (
        f"Message groups existence test failed for "
        f"'{logger.language.value}/{namespace_name}'.\n"
    )


@pytest.mark.parametrize(
    "language, namespace_name",
    TRANSLATED_CASES,
)
def test_message_groups_integrity(
    pivot: Logger, language: Language, namespace_name: Namespace
):
    logger = Logger(enabled=False, language=language)

    assert_message_groups_exists(
        pivot,
        logger,
        namespace_name,
    )


def assert_messages_exists(
    pivot: Logger,
    logger: Logger,
    namespace_name: Namespace,
    message_group_name: str,
):
    pivot_message_group = pivot.get_message_group(
        namespace=namespace_name,
        message_group=message_group_name,
    )
    logger_message_group = logger.get_message_group(
        namespace=namespace_name,
        message_group=message_group_name,
    )

    pivot_message_keys = set(pivot_message_group.keys())
    logger_message_keys = set(logger_message_group.keys())

    assert pivot_message_keys == logger_message_keys, (
        f"Message existence test failed for "
        f"'{logger.language.value}/{namespace_name}/{message_group_name}'.\n"
    )


@pytest.mark.parametrize(
    "language, namespace_name",
    TRANSLATED_CASES,
)
def test_messages_integrity(
    pivot: Logger, language: Language, namespace_name: Namespace
):
    logger = Logger(enabled=False, language=language)

    namespace = pivot.get_namespace(
        namespace=namespace_name,
    )

    for message_group_name, _ in namespace.items():
        assert_messages_exists(
            pivot,
            logger,
            namespace_name,
            message_group_name,
        )
