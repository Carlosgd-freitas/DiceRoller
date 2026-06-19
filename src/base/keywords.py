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
    CLEANSE = "CLEANSE"
    CONFUSE = "CONFUSE"
    CORRUPT = "CORRUPT"
    CURSE = "CURSE"
    DOOM = "DOOM"
    DRAIN = "DRAIN"
    EXECUTE = "EXECUTE"
    FOCUS = "FOCUS"
    FORTIFY = "FORTIFY"
    FRAGILE = "FRAGILE"
    FREEZE = "FREEZE"
    FROSTBURN = "FROSTBURN"
    HASTE = "HASTE"
    HEAL = "HEAL"
    IMMUNITY = "IMMUNITY"
    INVISIBLE = "INVISIBLE"
    INVULNERABLE = "INVULNERABLE"
    MANA = "MANA"
    MANA_REGEN = "MANA_REGEN"
    NOTHING = "NOTHING"
    OIL = "OIL"
    PIERCE = "PIERCE"
    POISON = "POISON"
    REGEN = "REGEN"
    REVIVE = "REVIVE"
    SACRED_BLOCK = "SACRED_BLOCK"
    SLEEP = "SLEEP"
    SLOW = "SLOW"
    STRENGTH = "STRENGTH"
    STUN = "STUN"
    TAUNT = "TAUNT"
    THORNS = "THORNS"
    WEAK = "WEAK"


def get_keyword(name: str) -> Keyword:
    """
    Gets a Keyword enum based on it's name.

    :param name: A Keyword's name.
    :type name: str

    :return: The keyword.
    :rtype: Keyword
    """
    for keyword in Keyword:
        if keyword.name.lower() == name.lower():
            return keyword

    return


def get_keyword_color(keyword: Keyword) -> ColorParams:
    background_color = None
    intensity = "BRIGHT"

    if keyword in [Keyword.ABSORB, Keyword.DRAIN, Keyword.REGEN]:
        foreground_color = Color.GRASS_GREEN
    elif keyword in [Keyword.ATTACK, Keyword.PIERCE]:
        foreground_color = Color.ORANGE
    elif keyword in [Keyword.BLEED]:
        foreground_color = Color.RED
        intensity = "DIM"
    elif keyword in [Keyword.BLIND, Keyword.STUN]:
        foreground_color = Color.GRAY
    elif keyword in [Keyword.BLOCK]:
        foreground_color = Color.SKY_BLUE
    elif keyword in [Keyword.BURN]:
        foreground_color = Color.RED
    elif keyword in [Keyword.CLEANSE]:
        foreground_color = Color.AERO
    elif keyword in [Keyword.CONFUSE]:
        foreground_color = Color.HOT_PINK
    elif keyword in [Keyword.CORRUPT]:
        foreground_color = Color.LILAC
    elif keyword in [Keyword.CURSE, Keyword.DOOM]:
        foreground_color = Color.VIOLET
    elif keyword in [Keyword.EXECUTE, Keyword.INVISIBLE, Keyword.OIL]:
        background_color = Color.GRAY
        foreground_color = Color.BLACK
        intensity = "BRIGHT"
    elif keyword in [Keyword.FOCUS]:
        foreground_color = Color.LEMON
    elif keyword in [Keyword.FORTIFY, Keyword.HASTE, Keyword.STRENGTH]:
        foreground_color = Color.SPRING_GREEN
    elif keyword in [Keyword.FRAGILE, Keyword.SLOW, Keyword.WEAK]:
        foreground_color = Color.TOMATO
    elif keyword in [Keyword.FREEZE, Keyword.FROSTBURN]:
        foreground_color = Color.SKY_BLUE
    elif keyword in [Keyword.HEAL]:
        foreground_color = Color.GREEN
    elif keyword in [Keyword.IMMUNITY, Keyword.NOTHING]:
        foreground_color = Color.WHITE
    elif keyword in [Keyword.INVULNERABLE, Keyword.REVIVE, Keyword.SACRED_BLOCK]:
        foreground_color = Color.GOLD
    elif keyword in [Keyword.MANA, Keyword.MANA_REGEN]:
        foreground_color = Color.BLUE
    elif keyword in [Keyword.POISON]:
        foreground_color = Color.EMERALD_GREEN
    elif keyword in [Keyword.SLEEP]:
        foreground_color = Color.METALLIC_BLUE
        intensity = "DIM"
    elif keyword in [Keyword.TAUNT]:
        foreground_color = Color.PINK
    elif keyword in [Keyword.THORNS]:
        foreground_color = Color.OLIVE
    else:
        foreground_color = None

    return {
        "background_color": background_color,
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
