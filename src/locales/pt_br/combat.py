"""PT-BR localization for combat module."""

from src.base.color import color_string

COMBAT = {
    "died": "morreu",
    "draw": "É um empate!",
    "round": "Rodada",
    "team": color_string("Time #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "Turno",
    "winner": "\nO time {team_name} é o vencedor!",
}
