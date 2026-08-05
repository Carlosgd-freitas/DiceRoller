"""Tests for data utility module methods."""

from src.base.data import next_value
from tests.utils import assert_conditions


def test_next_value():
    example = ["A", "B", "C"]

    conditions = [
        next_value(example, "A") == "B",
        next_value(example, "B") == "C",
        next_value(example, "C") == "A",
    ]

    assert_conditions(conditions)
