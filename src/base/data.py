"""Data utility functions."""

from typing import List, TypeVar

T = TypeVar("T")


def next_value(values: List[T], current_value: T) -> T:
    """
    Returns the next element of a list of selectable items, related to the current
    selected one. The end and start of the list are wrapped around.

    :param values: List of values.
    :type values: List[T]

    :param current_value: Current selected value of the list.
    :type current_value: T

    :return: Next selectable value of the list.
    :rtype: T
    """
    index = values.index(current_value)
    new_value = values[(index + 1) % len(values)]
    return new_value
