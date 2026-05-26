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
    COUNTER = "COUNTER"
    CURSE = "CURSE"
    DODGE = "DODGE"
    DRAIN = "DRAIN"
    FORTIFY = "FORTIFY"
    FRAGILE = "FRAGILE"
    FREEZE = "FREEZE"
    HASTE = "HASTE"
    HEAL = "HEAL"
    HEMORRAGY = "HEMORRAGY"
    HEX = "HEX"
    MANA = "MANA"
    MANA_REGEN = "MANA_REGEN"
    NOTHING = "NOTHING"
    PIERCE = "PIERCE"
    POISON = "POISON"
    REGEN = "REGEN"
    REVIVE = "REVIVE"
    SCORCH = "SCORCH"
    SLEEP = "SLEEP"
    SLOW = "SLOW"
    STRENGTHEN = "STRENGTHEN"
    STUN = "STUN"
    TAUNT = "TAUNT"
    THORNS = "THORNS"
    TOXIC = "TOXIC"
    WEAKEN = "WEAKEN"


def get_keyword_color(keyword: Keyword) -> ColorParams:
    intensity = "BRIGHT"

    if keyword in [Keyword.ABSORB, Keyword.DRAIN, Keyword.REGEN]:
        foreground_color = Color.GRASS_GREEN
    elif keyword in [Keyword.ATTACK, Keyword.PIERCE]:
        foreground_color = Color.ORANGE
    elif keyword in [Keyword.BLEED, Keyword.HEMORRAGY]:
        foreground_color = Color.BURGUNDY
        intensity = "DIM"
    elif keyword in [Keyword.BLIND, Keyword.COUNTER, Keyword.STUN]:
        foreground_color = Color.GRAY
    elif keyword in [Keyword.BLOCK, Keyword.DODGE]:
        foreground_color = Color.BLUE
    elif keyword in [Keyword.BURN, Keyword.SCORCH]:
        foreground_color = Color.RED
    elif keyword == Keyword.CLEANSE:
        foreground_color = Color.AERO
    elif keyword == [Keyword.CONFUSE, Keyword.TAUNT]:
        foreground_color = Color.HOT_PINK
    elif keyword in [Keyword.CURSE, Keyword.HEX]:
        foreground_color = Color.VIOLET
    elif keyword in [Keyword.FORTIFY, Keyword.HASTE, Keyword.STRENGTHEN]:
        foreground_color = Color.PINK
    elif keyword in [Keyword.FRAGILE, Keyword.SLOW, Keyword.WEAKEN]:
        foreground_color = Color.BEIGE
    elif keyword == Keyword.FREEZE:
        foreground_color = Color.SKY_BLUE
    elif keyword == Keyword.HEAL:
        foreground_color = Color.GREEN
    elif keyword in [Keyword.MANA, Keyword.MANA_REGEN]:
        foreground_color = Color.LILAC
    elif keyword == Keyword.REVIVE:
        foreground_color = Color.LEMON
    elif keyword in [Keyword.POISON, Keyword.TOXIC]:
        foreground_color = Color.EMERALD_GREEN
    elif keyword == Keyword.SLEEP:
        foreground_color = Color.METALLIC_BLUE
        intensity = "DIM"
    elif keyword == Keyword.THORNS:
        foreground_color = Color.OLIVE
    else:
        foreground_color = None

    return {
        "foreground_color": foreground_color,
        "intensity": intensity,
    }
