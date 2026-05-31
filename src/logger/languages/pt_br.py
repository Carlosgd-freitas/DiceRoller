from src.base.color import Color, color_string

ACTIONS = {
    "absorb": "ABSORVIDO",
    "attack": "ATACOU",
    "block": "BLOQUEADO",
    "drain": "DRENOU",
    "pierce": "PERFUROU",
}

ATTRIBUTES = {
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string("MANA", foreground_color=Color.BLUE),
}

COMBAT = {
    "death": "{name} morreu!",
    "draw": "É um empate!",
    "miss": "{name} errou o alvo!",
    "round": "║ Rodada #{round:<5} ║",
    "team": color_string("Time #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "\n> Turno: {name} <\n",
    "winner": "\nO time {team_name} é o vencedor!",
}

DAMAGE = {
    # Part 1: Base message
    "base": "{source} {action} {target}.",
    "base_self": "{source} {action} a si mesmo.",
    # Part 2: Defensive messages
    "absorb": "{absorbed_damage} de dano foi {action}.",
    "block": "{blocked_damage} de dano foi {action}.",
    # Part 3: Damage message
    "damage": "{damage} de dano foi infligido.",
}

EFFECT_ACTIVATION = {
    "bleed": "{target} recebeu {damage} de dano de {keyword}.",
    "burn": "{target} recebeu {damage} de dano de {keyword}.",
    "freeze": "{target} não pôde agir porque estava {status}.",
    "poison": "{target} recebeu {damage} de dano de {keyword}.",
    "mana_regen": "{target} restaurou {value} de {attribute} de si mesmo através da {keyword}.",
    "regen": "{target} restaurou {value} de {attribute} de si mesmo através da {keyword}.",
    "sleep": "{target} não pôde agir porque estava {status}.",
    "stun": "{target} não pôde agir porque estava {status}.",
    "thorns": "{target} recebeu {damage} de dano de {keyword}.",
}

EFFECT_EXECUTION = {
    "buff": "{source} fortaleceu {target} com {keyword} por {duration} turnos.",
    "buff_self": "{source} se fortaleceu com {keyword} por {duration} turnos.",
    "debuff": "{source} enfraqueceu {target} com {keyword} por {duration} turnos.",
    "debuff_self": "{source} se enfraqueceu com {keyword} por {duration} turnos.",
    "defensive": "{source} protegeu {target}. {target} recebeu {value} de {keyword}.",
    "defensive_self": "{source} se protegeu e recebeu {value} de {keyword}.",
    "deterioration": "{source} deteriorou {value} {attribute} de {target} através de {keyword}.",
    "deterioration_self": "{source} deteriorou {value} {attribute} de si mesmo através de {keyword}.",
    "nothing": "Nada aconteceu.",
    "nothing_self": "Nada aconteceu.",
    "restoration": "{source} restaurou {value} de {attribute} de {target} através de {keyword}.",
    "restoration_self": "{source} restaurou {value} de {attribute} de si mesmo através de {keyword}.",
}

EFFECT_REMOVAL = {
    "burn": "{target} teve sua {removed_keyword} apagada pelo efeito de {keyword}.",
    "freeze": "{target} teve seu {removed_keyword} derretido pelo efeito de {keyword}.",
    "sleep": "{target} acordou de seu {removed_keyword} pelo efeito de {keyword}.",
}

KEYWORDS = {
    "absorb": "ABSORÇÃO",
    "attack": "ATAQUE",
    "bleed": "SANGRAMENTO",
    "blind": "CEGUEIRA",
    "block": "BLOQUEIO",
    "burn": "QUEIMADURA",
    "confuse": "CONFUSÃO",
    "curse": "MALDIÇÃO",
    "drain": "DRENAR",
    "freeze": "CONGELAMENTO",
    "heal": "CURA",
    "mana_regen": "REGENERAÇÃO DE MANA",
    "mana": "MANA",
    "nothing": "NADA",
    "pierce": "PERFURAR",
    "poison": "ENVENENAMENTO",
    "regen": "REGENERAÇÃO",
    "sleep": "SONO",
    "stun": "ATORDOAMENTO",
    "thorns": "ESPINHOS",
}

STATUS = {
    "blind": "CEGO",
    "confuse": "CONFUSO",
    "freeze": "CONGELADO",
    "sleep": "DORMINDO",
    "stun": "ATORDOADO",
}
