"""PT-BR base localization module."""

from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string(
        "MANA",
        **get_keyword_color(Keyword.MANA),
    ),
    "speed": color_string(
        "VELOCIDADE", foreground_color=Color.WHITE, intensity="BRIGHT"
    ),
}

LEXICON = {
    "accuracy": "precisão",
    "area": "área",
    "areas": "áreas",
    "armor": "armadura",
    "armors": "armaduras",
    "column": "coluna",
    "columns": "colunas",
    "consumable": "consumable",
    "consumables": "consumables",
    "decay": "decaimento",
    "duration": "duração",
    "effect": "efeito",
    "effects": "efeitos",
    "equipment": "equipamento",
    "false": "falso",
    "item": "item",
    "items": "itens",
    "monster": "monstro",
    "monsters": "monstros",
    "name": "nome",
    "no": "não",
    "normal": "normal",
    "off": "desligado",
    "order": "ordem",
    "on": "ligado",
    "skill": "habilidade",
    "skills": "habilidades",
    "true": "verdadeiro",
    "type": "tipo",
    "value": "valor",
    "weapon": "arma",
    "weapons": "armas",
    "yes": "sim",
}
