from src.base.color import Color, color_string

ACTIONS = {
    "absorb": "ABOSRBED",
    "attack": "ATTACKED",
    "block": "BLOCKED",
    "drain": "DRAINED",
    "pierce": "PIERCED",
}

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string("MANA", foreground_color=Color.BLUE),
}

COMBAT = {
    "death": "{name} died!",
    "draw": "It's a draw!",
    "miss": "{name} missed their target!",
    "round": "║ Round #{round:<6} ║",
    "team": color_string("Team #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "\n> Turn: {name} <\n",
    "winner": "\nTeam {team_name} is the winner!",
}

DAMAGE = {
    # Part 1: Base message
    "base": "{source} {action} {target}.",
    "base_self": "{source} {action} itself.",
    # Part 2: Defensive messages
    "absorb": "{absorbed_damage} damage was {action}.",
    "block": "{blocked_damage} damage was {action}.",
    # Part 3: Damage message
    "damage": "{damage} damage was done.",
}

EFFECT_ACTIVATION = {
    "bleed": "{target} took {damage} damage from {keyword}.",
    "burn": "{target} took {damage} damage from {keyword}.",
    "freeze": "{target} could not act because it was {status}.",
    "poison": "{target} took {damage} damage from {keyword}.",
    "mana_regen": "{target} restored {value} {attribute} of itself through {keyword}.",
    "regen": "{target} restored {value} {attribute} of itself through {keyword}.",
    "sleep": "{target} could not act because it was {status}.",
    "stun": "{target} could not act because it was {status}.",
    "thorns": "{target} took {damage} damage from {keyword}.",
}

EFFECT_EXECUTION = {
    "buff": "{source} buffed {target} with {keyword} for {duration} turns.",
    "buff_self": "{source} buffed itself with {keyword} for {duration} turns.",
    "debuff": "{source} debuffed {target} with {keyword} for {duration} turns.",
    "debuff_self": "{source} debuffed itself with {keyword} for {duration} turns.",
    "defensive": "{source} protected {target}. {target} recieved {value} {keyword}.",
    "defensive_self": "{source} protected itself and recieved {value} {keyword}.",
    "deterioration": "{source} deteriored {value} {attribute} of {target} through {keyword}.",
    "deterioration_self": "{source} deteriored {value} {attribute} of itself through {keyword}.",
    "nothing": "Nothing happened.",
    "nothing_self": "Nothing happened.",
    "restoration": "{source} restored {value} {attribute} of {target} through {keyword}.",
    "restoration_self": "{source} restored {value} {attribute} of itself through {keyword}.",
}

EFFECT_REMOVAL = {
    "burn": "{target} had its {removed_keyword} put out by the effect of {keyword}.",
    "freeze": "{target} thawed from its {removed_keyword} by the effect of {keyword}.",
    "sleep": "{target} woke up from its {removed_keyword} by the effect of {keyword}.",
}

KEYWORDS = {
    "absorb": "ABOSRB",
    "attack": "ATTACK",
    "bleed": "BLEED",
    "blind": "BLIND",
    "block": "BLOCK",
    "burn": "BURN",
    "confuse": "CONFUSE",
    "curse": "CURSE",
    "drain": "DRAIN",
    "freeze": "FREEZE",
    "heal": "HEAL",
    "mana_regen": "MANA REGEN",
    "mana": "MANA",
    "nothing": "NOTHING",
    "pierce": "PIERCE",
    "poison": "POISON",
    "regen": "REGEN",
    "sleep": "SLEEP",
    "stun": "STUN",
    "thorns": "THORNS",
}

STATUS = {
    "blind": "BLIND",
    "confuse": "CONFUSED",
    "freeze": "FROZEN",
    "sleep": "ASLEEP",
    "stun": "STUNNED",
}
