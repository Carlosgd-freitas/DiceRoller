"""Utility functions for testing."""

from typing import List


def assert_conditions(conditions: List[bool]):
    not_passed = [
        str(index + 1) for index, condition in enumerate(conditions) if not condition
    ]

    n_not_passed = len(not_passed)
    not_passed = ", ".join(not_passed)

    assert all(
        conditions
    ), f"{n_not_passed} Conditions not passed (of {len(conditions)}): {not_passed}"
