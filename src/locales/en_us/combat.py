"""EN-US localization for combat module."""

from src.base.color import color_string

COMBAT = {
    "died": "died",
    "draw": "It's a draw!",
    "round": "Round",
    "team": color_string("Team #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "Turn",
    "winner": "\nTeam {team_name} is the winner!",
}
