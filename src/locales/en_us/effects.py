"""EN-US localization for effects module."""

ABSORB = {
    "name": "ABSORB",
    "description": "Reduces up to {value} recieved direct damage. Any blocked damage restores {hp}.",
    "action": "ABSORBED",
    "activation": "{defended_damage} damage was {defensive_action}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "ABSORBING",
}

ATTACK = {
    "name": "ATTACK",
    "description": "Deals {value} damage.",
    "action": "ATTACKED",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} {action} themselves.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

BLEED = {
    "name": "BLEED",
    "description": "Deals {value} damage every time the target rolls a dice.",
    "action": None,
    "activation": "{target} took {damage} damage from {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

BLIND = {
    "name": "BLIND",
    "description": "Reduces the accuracy of dice and skills that the target not use in themselves by {value_perc}%.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_keyword} anymore by the effect of {keyword}.",
    "status": "BLIND",
}

BLOCK = {
    "name": "BLOCK",
    "description": "Reduces up to {value} recieved direct damage.",
    "action": "BLOCKED",
    "activation": "{defended_damage} damage was {defensive_action}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

BURN = {
    "name": "BURN",
    "description": "Deals {value} damage every turn start. Removes {freeze}.",
    "action": None,
    "activation": "{target} took {damage} damage from {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} had its {removed_keyword} put out by the effect of {keyword}.",
    "status": "BURNED",
}

CLEANSE = {
    "name": "CLEANSE",
    "description": "Removes up to {value} debuffs from the target, starting from the oldest.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} removed {count} debuffs from {target} through {keyword}",
    "execution_self": "{source} removed {count} debuffs from themselves through {keyword}",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

CONFUSE = {
    "name": "CONFUSE",
    "description": "Makes the target use their dice and skills randomly.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "CONFUSED",
}

CORRUPT = {
    "name": "CORRUPT",
    "description": "Removes up to {value} buffs from the target, starting from the oldest.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} removed {count} buffs from {target} through {keyword}",
    "execution_self": "{source} removed {count} buffs from themselves through {keyword}",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

DOOM = {
    "name": "DOOM",
    "description": "Kills the target after {duration} turns.",
    "action": "DOOMED",
    "activation": "{target} met its {keyword}.",
    "countdown": "{duration} turns remain for {target} to meet its {keyword}.",
    "execution": "{source} {action} {target}. {target} will die in {duration} turns.",
    "execution_self": "{source} {action} themselves. {source} will die in {duration} turns.",
    "execution_fail": "{source} tried to {keyword} {target}, but",
    "execution_fail_self": "{source} tried to {keyword} themselves, but",
    "fail": None,
    "removal": None,
    "status": "DOOMED",
}

DRAIN = {
    "name": "DRAIN",
    "description": "Deals {value} damage. Any dealt damage restores {hp}.",
    "action": "DRAINED",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} {action} themselves.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

EXECUTE = {
    "name": "EXECUTE",
    "description": "Kills the target if its {hp} is less than or equal to {value_perc}% of it's max {hp}.",
    "action": "EXECUTED",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} {action} themselves.",
    "execution_fail": "{source} tried to {keyword} {target}, but",
    "execution_fail_self": "{source} tried to {keyword} themselves, but",
    "fail": None,
    "removal": None,
    "status": None,
}

FOCUS = {
    "name": "FOCUS",
    "description": "Increases the accuracy of dice and skills of the target by {value_perc}%.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} had its {removed_keyword} disturbed by the effect of {keyword}.",
    "status": None,
}

FORTIFY = {
    "name": "FORTIFY",
    "description": "Increases damage reduction from defensive effects by {value}.",
    "action": "FORTIFY",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_status} anymore by the effect of {keyword}.",
    "status": "FORTIFIED",
}

FRAGILE = {
    "name": "FRAGILE",
    "description": "Decreases damage reduction from defensive effects by {value}.",
    "action": "FRAGILIZED",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_status} anymore because of {keyword}.",
    "status": "FRAGILE",
}

FREEZE = {
    "name": "FREEZE",
    "description": "Makes target unable to act. Removes {burn}.",
    "action": None,
    "activation": "{source} could not act because it was {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} was {status}.",
    "removal": "{target} thawed from its {removed_keyword} by the effect of {keyword}.",
    "status": "FROZEN",
}

FROSTBURN = {
    "name": "FROSTBURN",
    "description": "Deals {value} damage every turn start.",
    "action": None,
    "activation": "{target} took {damage} damage from {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "FROSTBURNED",
}

HASTE = {
    "name": "HASTE",
    "description": "Increases the target speed by {value}.",
    "action": "HASTEN",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_status} anymore by the effect of {keyword}.",
    "status": "HASTY",
}

HEAL = {
    "name": "HEAL",
    "description": "Restores {value} {hp}.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} restored {value} {hp} of {target} through {keyword}.",
    "execution_self": "{source} restored {value} {hp} of themselves through {keyword}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

IMMUNITY = {
    "name": "IMMUNITY",
    "description": "Makes target immune to other effects. Any effects the target is under will still continue to be applied.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} granted {keyword} of {count} effects to {target}",
    "execution_self": "{source} granted {keyword} of {count} effects to themselves",
    "execution_fail": "{source} tried to turn {target} {status}, but",
    "execution_fail_self": "{source} tried to turn themselves {status}, but",
    "fail": "{target} was {status}.",
    "removal": None,
    "status": "IMMUNE",
}

INVISIBLE = {
    "name": "INVISIBLE",
    "description": "Makes the target untargetable by enemies.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} turned {target} {keyword} for {duration} turns.",
    "execution_self": "{source} turned themselves {keyword} for {duration} turns.",
    "execution_fail": "{source} tried to turn {target} {keyword}, but",
    "execution_fail_self": "{source} tried to turn themselves {keyword}, but",
    "fail": None,
    "removal": None,
    "status": None,
}

INVULNERABLE = {
    "name": "INVULNERABLE",
    "description": "Negates any damage that would be done to the target.",
    "action": None,
    "activation": "{defended_damage} damage was negated because {target} was {defensive_status}.",
    "countdown": None,
    "execution": "{source} turned {target} {keyword} for {duration} turns.",
    "execution_self": "{source} turned themselves {keyword} for {duration} turns.",
    "execution_fail": "{source} tried to turn {target} {keyword}, but",
    "execution_fail_self": "{source} tried to turn themselves {keyword}, but",
    "fail": None,
    "removal": None,
    "status": "INVULNERABLE",
}

MANA_REGEN = {
    "name": "MANA REGEN",
    "description": "Increases {mana} by {value} every turn start.",
    "action": None,
    "activation": "{target} restored {value} {mana} of themselves through {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

MANA = {
    "name": "MANA",
    "description": "Increases {mana} by {value}.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} restored {value} {mana} of {target} through {keyword}.",
    "execution_self": "{source} restored {value} {mana} of themselves through {keyword}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

NOTHING = {
    "name": "NOTHING",
    "description": "Does nothing.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "Nothing happened.",
    "execution_self": "Nothing happened.",
    "execution_fail": "Nothing would happen, but {source}",
    "execution_fail_self": "Nothing would happen, but {source}",
    "fail": None,
    "removal": None,
    "status": None,
}

OIL = {
    "name": "OIL",
    "description": "Reduces the target speed and increases damage dealt by {burn} by {value}.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

PAIN = {
    "name": "PAIN",
    "description": "Deals {value} damage to self. Ignores defensive effects.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} inflicted {value} damage to {target} through {keyword}.",
    "execution_self": "{source} inflicted {value} damage to themselves through {keyword}.",
    "execution_fail": "{source} would cause {keyword} on {target}, but",
    "execution_fail_self": "{source} would feel {keyword}, but",
    "fail": None,
    "removal": None,
    "status": None,
}

PIERCE = {
    "name": "PIERCE",
    "description": "Deals {value} damage. Ignores {absorb}, {block} and {sacred_block}.",
    "action": "PIERCED",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} {action} themselves.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

POISON = {
    "name": "POISON",
    "description": "Deals {value} damage every turn start.",
    "action": None,
    "activation": "{target} took {damage} damage from {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

REGEN = {
    "name": "REGEN",
    "description": "Restores {value} {hp} every turn start.",
    "action": None,
    "activation": "{target} restored {value} {hp} of themselves through {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

REPEL = {
    "name": "REPEL",
    "description": "Decreases the pririority of the target for enemies.",
    "action": "REPELLED",
    "activation": None,
    "countdown": None,
    "execution": "{source} made {target} {keyword} the enemies for {duration} turns.",
    "execution_self": "{source} {action} the enemies for {duration} turns.",
    "execution_fail": "{source} tried to make {target} {keyword} the enemies, but",
    "execution_fail_self": "{source} tried to {keyword} the enemies, but",
    "fail": None,
    "removal": "{target} stopped its {removed_keyword} by the effect of {keyword}.",
    "status": "REPELLING",
}

REVIVE = {
    "name": "REVIVE",
    "description": "Revives a dead target and heals it by {value_perc}% of it's max {hp}.",
    "action": "REVIVED",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}. {target} was healed by {value_perc}% of its max {hp}.",
    "execution_self": "{source} {action} themselves and was healed by {value_perc}% of its max {hp}.",
    "execution_fail": "{source} tried to {keyword} {target}, but",
    "execution_fail_self": "{source} tried to {keyword} themselves, but",
    "fail": None,
    "removal": None,
    "status": None,
}

SACRED_BLOCK = {
    "name": "SACRED BLOCK",
    "description": "Reduces all recieved direct damage up to {value} times.",
    "action": "SACRED BLOCKED",
    "activation": "{defended_damage} damage was {defensive_action}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

SLEEP = {
    "name": "SLEEP",
    "description": "Makes target unable to act. Any direct damage will wake up the target.",
    "action": None,
    "activation": "{source} could not act because it was {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} was {status}.",
    "removal": "{target} woke up from its {removed_keyword} by the effect of {keyword}.",
    "status": "ASLEEP",
}

SLOW = {
    "name": "SLOW",
    "description": "Reduces the target speed by {value}.",
    "action": "SLOWED",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_status} anymore by the effect of {keyword}.",
    "status": "SLOWED",
}

STRENGTH = {
    "name": "STRENGTH",
    "description": "Increases damage dealt by offensive effects by {value}.",
    "action": "STRENGTHEN",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_status} anymore by the effect of {keyword}.",
    "status": "STRONG",
}

STUN = {
    "name": "STUN",
    "description": "Makes target unable to act.",
    "action": None,
    "activation": "{source} could not act because it was {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} was {status}.",
    "removal": None,
    "status": "STUNNED",
}

TAUNT = {
    "name": "TAUNT",
    "description": "Increases the pririority of the target for enemies.",
    "action": "TAUNTED",
    "activation": None,
    "countdown": None,
    "execution": "{source} made {target} {keyword} the enemies for {duration} turns.",
    "execution_self": "{source} {action} the enemies for {duration} turns.",
    "execution_fail": "{source} tried to make {target} {keyword} the enemies, but",
    "execution_fail_self": "{source} tried to {keyword} the enemies, but",
    "fail": None,
    "removal": "{target} stopped its {removed_keyword} by the effect of {keyword}.",
    "status": "TAUNTING",
}

THORNS = {
    "name": "THORNS",
    "description": "When attacked directly, deals {value} damage to the attacker.",
    "action": None,
    "activation": "{target} took {damage} damage from {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

WEAK = {
    "name": "WEAK",
    "description": "Reduces damage dealt by offensive effects by {value}.",
    "action": "WEAKEN",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} is not {removed_keyword} anymore by the effect of {keyword}.",
    "status": "WEAKNESS",
}
