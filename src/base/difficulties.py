"""Difficulties module."""

from enum import Enum


class Difficulty(Enum):
    """Game difficulty level."""

    EASY = 0
    NORMAL = 1
    HARD = 2
    EXPERT = 3
    MASTER = 4
    NIGHTMARE = 5
