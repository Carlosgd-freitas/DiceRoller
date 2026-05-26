from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color

MESSAGES = {
    # Combat
    "death": "{name} morreu!",
    "draw": "É um empate!",
    "round": "║ Rodada #{round:<5} ║",
    "team": (color_string("Time #{index}: {team_name}", intensity="BRIGHT")),
    "turn": "\n> Turno: {name} <\n",
    "winner": "\nO time {team_name} é o vencedor!",
    # Persistent Status Effects
    "status_block": "BLOQUEIO",
    # Effects Activating / Applying
    "attack": (
        "{source} "
        + color_string(
            "ATACOU",
            foreground_color=get_keyword_color(Keyword.ATTACK)["foreground_color"],
            intensity=get_keyword_color(Keyword.ATTACK)["intensity"],
        )
        + " {target} e causou {damage} de dano."
    ),
    "attack_self": (
        "{source} se "
        + color_string(
            "ATACOU",
            foreground_color=get_keyword_color(Keyword.ATTACK)["foreground_color"],
            intensity=get_keyword_color(Keyword.ATTACK)["intensity"],
        )
        + " e causou {damage} de dano.",
    ),
    "block": (
        "{source} protegeu {target}. {target} recebeu {value} de "
        + color_string(
            "BLOQUEIO",
            foreground_color=get_keyword_color(Keyword.BLOCK)["foreground_color"],
            intensity=get_keyword_color(Keyword.BLOCK)["intensity"],
        )
        + "."
    ),
    "block_self": (
        "{source} se protegeu e recebeu {value} de "
        + color_string(
            "BLOQUEIO",
            foreground_color=get_keyword_color(Keyword.BLOCK)["foreground_color"],
            intensity=get_keyword_color(Keyword.BLOCK)["intensity"],
        )
        + "."
    ),
}
