"""EN-US localization for combat module."""

ACTIONS = {"skip_turn": "{name} decided to do nothing."}

COMBAT = {
    "ai": "AI",
    "damage": "{damage} damage was done.",
    "died": "died",
    "draw": "It's a draw!",
    "player": "PLAYER",
    "round": "Round",
    "team": "Team",
    "turn": "Turn",
    "winner": "\nTeam {team_name} is the winner!",
}

FAILS = {
    "act_disabled": "they could not act.",
    "default": "failed.",
    "non-persistable": "failed.",
    "source_alive": "they were alive.",
    "source_dead": "they were dead.",
    "source_freeze": "they were {fail_status}.",
    "source_immunity": "they were {fail_status}.",
    "source_miss": "missed itself.",
    "source_sleep": "they were {fail_status}.",
    "source_stun": "they were {fail_status}.",
    "target_alive": "{target} was alive.",
    "target_dead": "{target} was dead.",
    "target_freeze": "{target} was {fail_status}.",
    "target_immunity": "{target} was {fail_status}.",
    "target_miss": "missed the target.",
    "target_sleep": "{target} was {fail_status}.",
    "target_stun": "{target} was {fail_status}.",
}
