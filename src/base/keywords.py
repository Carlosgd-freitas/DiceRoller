"""Keyword module."""

from enum import Enum

from src.base.color import Color, ColorParams


class Keyword(Enum):
    """Effect keywords (identifiers)."""

    ABSORB = "ABSORB"
    ATTACK = "ATTACK"
    BLEED = "BLEED"
    BLIND = "BLIND"
    BLOCK = "BLOCK"
    BURN = "BURN"
    CONFUSE = "CONFUSE"
    CURSE = "CURSE"
    DOOM = "DOOM"
    DRAIN = "DRAIN"
    EXECUTE = "EXECUTE"
    FREEZE = "FREEZE"
    HEAL = "HEAL"
    INVISIBLE = "INVISIBLE"
    MANA = "MANA"
    MANA_REGEN = "MANA_REGEN"
    NOTHING = "NOTHING"
    PIERCE = "PIERCE"
    POISON = "POISON"
    REGEN = "REGEN"
    REVIVE = "REVIVE"
    SACRED_BLOCK = "SACRED_BLOCK"
    SLEEP = "SLEEP"
    STUN = "STUN"
    THORNS = "THORNS"


def get_keyword_color(keyword: Keyword) -> ColorParams:
    background_color = None
    intensity = "BRIGHT"

    if keyword in [Keyword.ABSORB, Keyword.DRAIN, Keyword.REGEN]:
        foreground_color = Color.GRASS_GREEN
    elif keyword in [Keyword.ATTACK, Keyword.PIERCE]:
        foreground_color = Color.ORANGE
    elif keyword in [Keyword.BLEED]:
        foreground_color = Color.BURGUNDY
        intensity = "DIM"
    elif keyword in [Keyword.BLIND, Keyword.STUN]:
        foreground_color = Color.GRAY
    elif keyword in [Keyword.BLOCK]:
        foreground_color = Color.BLUE
    elif keyword in [Keyword.BURN]:
        foreground_color = Color.RED
    elif keyword in [Keyword.CONFUSE]:
        foreground_color = Color.HOT_PINK
    elif keyword in [Keyword.CURSE, Keyword.DOOM]:
        foreground_color = Color.VIOLET
    elif keyword in [Keyword.EXECUTE, Keyword.INVISIBLE]:
        background_color = Color.GRAY
        foreground_color = Color.BLACK
        intensity = "BRIGHT"
    elif keyword in [Keyword.FREEZE]:
        foreground_color = Color.SKY_BLUE
    elif keyword in [Keyword.HEAL]:
        foreground_color = Color.GREEN
    elif keyword in [Keyword.MANA, Keyword.MANA_REGEN]:
        foreground_color = Color.LILAC
    elif keyword in [Keyword.POISON]:
        foreground_color = Color.EMERALD_GREEN
    elif keyword in [Keyword.REVIVE, Keyword.SACRED_BLOCK]:
        foreground_color = Color.LEMON
    elif keyword in [Keyword.SLEEP]:
        foreground_color = Color.METALLIC_BLUE
        intensity = "DIM"
    elif keyword in [Keyword.THORNS]:
        foreground_color = Color.OLIVE
    else:
        foreground_color = None

    return {
        "background_color": background_color,
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
