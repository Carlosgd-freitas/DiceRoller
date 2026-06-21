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

WORDS = {
    "accuracy": "accuracy",
    "area": "area",
    "areas": "areas",
    "decay": "decay",
    "duration": "duration",
    "item": "item",
    "items": "items",
    "effect": "effect",
    "effects": "effects",
    "skill": "skill",
    "skills": "skills",
    "monster": "monster",
    "monsters": "monsters",
    "value": "value",
}
