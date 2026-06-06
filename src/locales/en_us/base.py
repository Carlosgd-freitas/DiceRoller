from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string(
        "MANA",
        **get_keyword_color(Keyword.MANA),
    ),
}

WORDS = {
    "area": "area",
    "areas": "areas",
    "item": "item",
    "items": "items",
    "effect": "effect",
    "effects": "effects",
    "skill": "skill",
    "skills": "skills",
    "monster": "monster",
    "monsters": "monsters",
}
