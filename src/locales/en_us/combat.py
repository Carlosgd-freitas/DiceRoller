from src.base.color import color_string

COMBAT = {
    "death": "{name} died!",
    "draw": "It's a draw!",
    "round": "Round #{round:<6}",
    "team": color_string("Team #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "Turn",
    "winner": "\nTeam {team_name} is the winner!",
}
