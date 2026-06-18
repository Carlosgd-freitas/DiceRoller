"""Rarities module."""

from enum import Enum

from src.base.color import Color, ColorParams


class Rarity(Enum):
    """Rarity."""

    JUNK = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


def get_rarity_color(rarity: Rarity) -> ColorParams:
    background_color = None
    intensity = "BRIGHT"

    if rarity == Rarity.JUNK:
        foreground_color = Color.GRAY
    elif rarity == Rarity.COMMON:
        foreground_color = Color.WHITE
    elif rarity == Rarity.UNCOMMON:
        foreground_color = Color.GREEN
    elif rarity == Rarity.RARE:
        foreground_color = Color.BLUE
    elif rarity == Rarity.EPIC:
        foreground_color = Color.RED
    elif rarity == Rarity.LEGENDARY:
        foreground_color = Color.GOLD
    else:
        foreground_color = None

    return {
        "background_color": background_color,
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
