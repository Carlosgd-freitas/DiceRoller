from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string(
        "MANA",
        foreground_color=get_keyword_color(Keyword.MANA)["foreground_color"],
        intensity=get_keyword_color(Keyword.MANA)["intensity"],
    ),
}

WORDS = {
    "area": "área",
    "areas": "áreas",
    "item": "item",
    "items": "itens",
    "effect": "efeito",
    "effects": "efeitos",
    "skill": "habilidade",
    "skills": "habilidades",
    "monster": "monstro",
    "monsters": "monstros",
}
