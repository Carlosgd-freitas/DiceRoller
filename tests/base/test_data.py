"""Tests for data utility module methods."""

from src.base.data import (
    next_value,
    previous_value,
)
from tests.utils import assert_conditions


def test_previous_value():
    example = ["A", "B", "C"]

    conditions = [
        previous_value(example, "A") == "C",
        previous_value(example, "B") == "A",
        previous_value(example, "C") == "B",
    ]

    assert_conditions(conditions)


def test_next_value():
    example = ["A", "B", "C"]

    conditions = [
        next_value(example, "A") == "B",
        next_value(example, "B") == "C",
        next_value(example, "C") == "A",
    ]

    assert_conditions(conditions)
