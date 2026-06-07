"""PT-BR localization for combat module."""

from src.base.color import color_string

COMBAT = {
    "death": "{name} morreu!",
    "draw": "É um empate!",
    "round": "Rodada #{round:<5}",
    "team": color_string("Time #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "Turno",
    "winner": "\nO time {team_name} é o vencedor!",
}
