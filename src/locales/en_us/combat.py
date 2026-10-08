"""EN-US localization for combat module."""

ACTIONS = {
    "roll_dice": "{name} rolled their dice and got:",
    "skill": "{monster_name} used {skill_name} and got:",
    "consumable": "{monster_name} used {consumable_name} and got:",
    "skip_turn": "{name} decided to do nothing.",
    "no_roll_dice": "{name} don't have dice to roll.",
    "no_skills": "{name} can't use any skills.",
    "no_consumables": "There are no consumables for {name} to use.",
    "no_equipment": "There are no equipment for {name}.",
    "no_show_details": "{name} can't see the details of anything!",
    "no_skip_turn": "{name} must do something!",
}

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
    "delay": "no effects could be extended.",
    "non-persistable": "it was ineffective.",
    "source_alive": "they were alive.",
    "source_dead": "died before they could do that.",
    "source_freeze": "they were {fail_status}.",
    "source_immunity": "they were {fail_status}.",
    "source_miss": "missed itself.",
    "source_resistance": "they {fail_action}.",
    "source_sleep": "they were {fail_status}.",
    "source_stun": "they were {fail_status}.",
    "target_alive": "{target} was alive.",
    "target_dead": "{target} was dead.",
    "target_freeze": "{target} was {fail_status}.",
    "target_immunity": "{target} was {fail_status}.",
    "target_resistance": "{target} {fail_action}.",
    "target_miss": "missed the target.",
    "target_sleep": "{target} was {fail_status}.",
    "target_stun": "{target} was {fail_status}.",
}

ORDER = {
    "faster": "FASTER",
    "order": "Combat Order",
    "sequential": "SEQUENTIAL",
    "shuffle": "SHUFFLE",
    "slower": "SLOWER",
}
