"""PT-BR base localization module."""

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
    "accuracy": "precisão",
    "area": "área",
    "areas": "áreas",
    "decay": "decaimento",
    "duration": "duração",
    "item": "item",
    "items": "itens",
    "effect": "efeito",
    "effects": "efeitos",
    "skill": "habilidade",
    "skills": "habilidades",
    "monster": "monstro",
    "monsters": "monstros",
    "value": "valor",
}
