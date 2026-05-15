"""Utility functions for testing."""

from typing import List


def assert_conditions(conditions: List[bool]):
    not_passed = [
        str(index) for index, condition in enumerate(conditions) if not condition
    ]

    not_passed = ", ".join(not_passed)

    assert all(conditions), f"Conditions not passed: {not_passed}"
