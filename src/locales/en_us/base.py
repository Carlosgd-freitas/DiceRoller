"""EN-US base localization module."""

from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string(
        "MANA",
        **get_keyword_color(Keyword.MANA),
    ),
    "speed": color_string("SPEED", foreground_color=Color.WHITE, intensity="BRIGHT"),
}

LEXICON = {
    "accuracy": "accuracy",
    "area": "area",
    "areas": "areas",
    "column": "column",
    "columns": "columns",
    "decay": "decay",
    "duration": "duration",
    "effect": "effect",
    "effects": "effects",
    "false": "false",
    "item": "item",
    "items": "items",
    "monster": "monster",
    "monsters": "monsters",
    "name": "name",
    "no": "no",
    "normal": "normal",
    "off": "off",
    "order": "order",
    "on": "on",
    "skill": "skill",
    "skills": "skills",
    "type": "type",
    "true": "true",
    "value": "value",
    "yes": "yes",
}
