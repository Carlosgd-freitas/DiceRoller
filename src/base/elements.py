"""Element types for effects, items, skills, resistances, etc."""

from enum import Enum


class Element(Enum):
    DARKNESS = "DARKNESS"
    EARTH = "EARTH"
    ELECTRIC = "ELECTRIC"
    FIRE = "FIRE"
    ICE = "ICE"
    LIGHT = "LIGHT"
    NORMAL = "NORMAL"
    WATER = "WATER"
    WIND = "WIND"
