"""EN-US localization for effects module."""

ACTIONS = {
    "absorb": "ABSORBED",
    "attack": "ATTACKED",
    "block": "BLOCKED",
    "drain": "DRAINED",
    "execute": "EXECUTED",
    "pierce": "PIERCED",
    "revive": "REVIVED",
}

ACTIVATION = {
    "bleed": "{target} took {damage} damage from {keyword}.",
    "burn": "{target} took {damage} damage from {keyword}.",
    "doom": "{target} met its {keyword}.",
    "freeze": "{target} could not act because it was {status}.",
    "poison": "{target} took {damage} damage from {keyword}.",
    "mana_regen": "{target} restored {value} {attribute} of itself through {keyword}.",
    "regen": "{target} restored {value} {attribute} of itself through {keyword}.",
    "sleep": "{target} could not act because it was {status}.",
    "stun": "{target} could not act because it was {status}.",
    "thorns": "{target} took {damage} damage from {keyword}.",
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

COMPENDIUM = {
    "title": "Effect Compendium",
    "next_item": "Next Effect",
    "previous_item": "Previous Effect",
    "select_item": "Select an effect (or [0] to cancel)",
    "show_item_details": "See Effect Details",
}

DESCRIPTION = {
    "absorb": "Reduces up to {value} recieved damage. Any blocked damage restores {hp}.",
    "attack": "Deals {value} damage.",
    "bleed": "Deals {value} damage every time the target rolls a dice.",
    "blind": "Increases the miss chance of target dice and skills by {value_perc}%.",
    "block": "Reduces up to {value} recieved damage.",
    "burn": "Deals {value} damage every turn start. Removes {freeze}.",
    "confuse": "Makes the target use their dice and skills randomly.",
    "curse": "Deals {value} damage to self. Ignores defensive effects.",
    "doom": "Kills the target after {duration} turns.",
    "drain": "Deals {value} damage. Any dealt damage restores {hp}.",
    "execute": "Kills the target if its' {hp} is less than or equal to {value_perc}% of it's max {hp}.",
    "freeze": "Makes target unable to act. Removes {burn}.",
    "heal": "Restores {value} {hp}.",
    "mana_regen": "Increases {mana} by {value} every turn start.",
    "mana": "Increases {mana} by {value}.",
    "nothing": "Does nothing.",
    "pierce": "Deals {value} damage. Ignores defensive effects.",
    "poison": "Deals {value} damage every turn start.",
    "regen": "Restores {value} {hp} every turn start.",
    "revive": "Revives a dead target and heals it by {value_perc}% of it's max {hp}.",
    "sleep": "Makes target unable to act. Any direct damage will wake up the target.",
    "stun": "Makes target unable to act.",
    "thorns": "When attacked directly, deals {damage} damage to the attacker.",
}

EXECUTION = {
    # Effect keywords
    "execute": "{source} {action} {target}.",
    "execute_self": "{source} {action} itself.",
    "revive": "{source} {action} {target}. {target} was healed by {value_perc}% of its max {hp}.",
    "revive_self": "{source} {action} itself and was healed by {value_perc}% of its max {hp}.",
    # Effect types
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

EXECUTION_FAIL = {
    # Effect keywords
    "execute": "{source} tried to {keyword} {target}, but",
    "execute_self": "{source} tried to {keyword} itself, but",
    "revive": "{source} tried to {keyword} {target}, but",
    "revive_self": "{source} tried to {keyword} itself, but",
    # Effect types
    "buff": "{source} tried to buff {target} with {keyword}, but",
    "buff_self": "{source} tried to buff itself with {keyword}, but",
    "debuff": "{source} tried to debuff {target} with {keyword}, but",
    "debuff_self": "{source} tried to debuff itself with {keyword}, but",
    "defensive": "{source} tried to protect {target} with {keyword}, but",
    "defensive_self": "{source} tried to protect itself with {keyword}, but",
    "deterioration": "{source} tried to deteriorate {target} with {keyword}, but",
    "deterioration_self": "{source} tried to deteriorate itself with {keyword}, but",
    "nothing": "Nothing would happen, but {source}",
    "nothing_self": "Nothing would happen, but {source}",
    "offensive": "{source} tried to {keyword} {target}, but",
    "offensive_self": "{source} tried to {keyword} itself, but",
    "restoration": "{source} tried to restore {target} with {keyword}, mas",
    "restoration_self": "{source} tried to restore itself with {keyword}, mas",
}

FAILS = {
    "alive": "{target} was alive.",
    "alive_self": "it was alive.",
    "dead": "{target} was dead.",
    "dead_self": "it was dead.",
    "default": "failed.",
    "default_self": "failed.",
    "miss": "missed the target.",
    "miss_self": "missed itself.",
}

KEYWORDS = {
    "absorb": "ABSORB",
    "attack": "ATTACK",
    "bleed": "BLEED",
    "blind": "BLIND",
    "block": "BLOCK",
    "burn": "BURN",
    "confuse": "CONFUSE",
    "curse": "CURSE",
    "doom": "DOOM",
    "drain": "DRAIN",
    "execute": "EXECUTE",
    "freeze": "FREEZE",
    "heal": "HEAL",
    "mana_regen": "MANA REGEN",
    "mana": "MANA",
    "nothing": "NOTHING",
    "pierce": "PIERCE",
    "poison": "POISON",
    "regen": "REGEN",
    "revive": "REVIVE",
    "sleep": "SLEEP",
    "stun": "STUN",
    "thorns": "THORNS",
}

REMOVAL = {
    "burn": "{target} had its {removed_keyword} put out by the effect of {keyword}.",
    "freeze": "{target} thawed from its {removed_keyword} by the effect of {keyword}.",
    "sleep": "{target} woke up from its {removed_keyword} by the effect of {keyword}.",
}

STATUS = {
    "blind": "BLIND",
    "confuse": "CONFUSED",
    "freeze": "FROZEN",
    "sleep": "ASLEEP",
    "stun": "STUNNED",
}

TYPES = {
    "buff": "BUFF",
    "debuff": "DEBUFF",
    "defensive": "DEFENSIVE",
    "deterioration": "DETERIORATION",
    "nothing": "NOTHING",
    "offensive": "OFFENSIVE",
    "restoration": "RESTORATION",
}
