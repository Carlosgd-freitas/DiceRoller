from src.base.color import color_string
from src.base.keywords import Keyword, get_keyword_color

MESSAGES = {
    # Combat
    "death": "{name} died!",
    "draw": "It's a draw!",
    "round": "║ Round #{round:<6} ║",
    "team": (color_string("Team #{index}: {team_name}", intensity="BRIGHT")),
    "turn": "\n> Turn: {name} <\n",
    "winner": "\nTeam {team_name} is the winner!",
    # Persistent Status Effects
    "status_block": "BLOCK",
    # Effects Activating / Applying
    "attack": (
        "{source} "
        + color_string(
            "ATTACKED",
            foreground_color=get_keyword_color(Keyword.ATTACK)["foreground_color"],
            intensity=get_keyword_color(Keyword.ATTACK)["intensity"],
        )
        + " {target} and caused {damage} damage."
    ),
    "attack_self": (
        "{source} "
        + color_string(
            "ATTACKED",
            foreground_color=get_keyword_color(Keyword.ATTACK)["foreground_color"],
            intensity=get_keyword_color(Keyword.ATTACK)["intensity"],
        )
        + " itself and caused {damage} damage.",
    ),
    "block": (
        "{source} protected {target}. {target} recieved {value} "
        + color_string(
            "BLOCK",
            foreground_color=get_keyword_color(Keyword.BLOCK)["foreground_color"],
            intensity=get_keyword_color(Keyword.BLOCK)["intensity"],
        )
        + "."
    ),
    "block_self": (
        "{source} protected itself and recieved {value} "
        + color_string(
            "BLOCK",
            foreground_color=get_keyword_color(Keyword.BLOCK)["foreground_color"],
            intensity=get_keyword_color(Keyword.BLOCK)["intensity"],
        )
        + "."
    ),
}
