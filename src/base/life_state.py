"""LifeState module."""

from enum import Enum


class LifeState(Enum):
    """State of life."""

    ALIVE = "ALIVE"
    ANY = "ANY"
    DEAD = "DEAD"
