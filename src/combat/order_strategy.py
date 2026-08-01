"""Order Strategy module."""

from enum import Enum


class OrderStrategy(Enum):
    """
    Strategy when definining monsters turn order in combat.

    * ``FASTER``: monsters act from highest to lowest speed
    * ``SEQUENTIAL``: monsters act in the order they are provided
    * ``SHUFFLE``: monsters act in random order
    * ``SLOWER``: monsters act from lowest to highest speed
    """

    FASTER = "FASTER"
    SEQUENTIAL = "SEQUENTIAL"
    SHUFFLE = "SHUFFLE"
    SLOWER = "SLOWER"
