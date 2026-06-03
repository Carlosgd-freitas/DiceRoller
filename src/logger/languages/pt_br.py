from src.base.color import Color, color_string
from src.base.keywords import Keyword, get_keyword_color

ACTIONS = {
    "absorb": "ABSORVIDO",
    "attack": "ATACOU",
    "block": "BLOQUEADO",
    "drain": "DRENOU",
    "pierce": "PERFUROU",
    "revive": "REVIVEU",
}

ATTRIBUTES = {
    "effects": "efeitos",
    "hp": color_string("HP", foreground_color=Color.RED),
    "mana": color_string(
        "MANA",
        foreground_color=get_keyword_color(Keyword.MANA)["foreground_color"],
        intensity=get_keyword_color(Keyword.MANA)["intensity"],
    ),
}

COMBAT = {
    "death": "{name} morreu!",
    "draw": "É um empate!",
    "round": "║ Rodada #{round:<5} ║",
    "team": color_string("Time #{index}: {team_name}", intensity="BRIGHT"),
    "turn": "Turno",
    "winner": "\nO time {team_name} é o vencedor!",
}

DAMAGE = {
    # Part 1: Base message
    "base": "{source} {action} {target}.",
    "base_self": "{source} se {action}.",
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

EFFECT_DESCRIPTION = {
    "absorb": "Reduz até {value} de dano recebido. Qualquer dano bloqueado restaura {hp}.",
    "attack": "Inflige {value} de dano.",
    "bleed": "Inflige {value} de dano toda vez que o alvo rola um dado.",
    "blind": "Aumenta a chance de erro dos dados e habilidades do alvo em {value_perc}%.",
    "block": "Reduz até {value} de dano recebido.",
    "burn": "Inflige {value} de dano em todo início de turno. Remove {FREEZE}.",
    "confuse": "Faz com que o alvo use seus dados e habilidades aleatoriamente.",
    "curse": "Inflige {value} de dano a si mesmo. Ignora efeitos defensivos.",
    "drain": "Inflige {value} de dano. Qualquer dano infligido restaura {hp}.",
    "freeze": "Impede que o alvo aja. Remove {BURN}.",
    "heal": "Restaura {value} {hp}.",
    "mana_regen": "Aumenta {mana} em {value} em todo início de turno.",
    "mana": "Aumenta {mana} em {value}.",
    "nothing": "Não faz nada.",
    "pierce": "Inflige {value} de dano. Ignora efeitos defensivos.",
    "poison": "Inflige {value} de dano em todo início de turno.",
    "regen": "Restaura {value} {hp} em todo início de turno.",
    "revive": "Revive um alvo morto e o cura em {value_perc}% de seu HP máximo.",
    "sleep": "Impede que o alvo aja. Qualquer dano direto irá acordar o alvo.",
    "stun": "Impede que o alvo aja.",
    "thorns": "Quando atacado diretamente, inflige {damage} de dano ao atacante.",
}

EFFECT_EXECUTION = {
    # Effect keywords
    "revive": "{source} {action} {target}. {target} foi curado em {value_perc}% de seu {hp} máximo.",
    "revive_self": "{source} {action} a si mesmo e se curou em {value_perc}% de seu {hp} máximo.",
    # Effect types
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

EFFECT_EXECUTION_FAIL = {
    # Effect keywords
    "revive": "{source} tentou {keyword} {target}, mas",
    "revive_self": "{source} tentou se {keyword}, mas",
    # Effect types
    "buff": "{source} tentou fortalecer {target} com {keyword}, mas",
    "buff_self": "{source} tentou se fortalecer com {keyword}, mas",
    "debuff": "{source} tentou enfraquecer {target} com {keyword}, mas",
    "debuff_self": "{source} tentou se enfraquecer com {keyword}, mas",
    "defensive": "{source} tentou proteger {target} com {keyword}, mas",
    "defensive_self": "{source} tentou se proteger com {keyword}, mas",
    "deterioration": "{source} tentou deteriorar {target} com {keyword}, mas",
    "deterioration_self": "{source} tentou se deteriorar com {keyword}, mas",
    "nothing": "Nada aconteceria, mas {source}",
    "nothing_self": "Nada aconteceria, mas {source}",
    "offensive": "{source} tentou {keyword} {target}, mas",
    "offensive_self": "{source} tentou se {keyword}, mas",
    "restoration": "{source} tentou restaurar {target} com {keyword}, mas",
    "restoration_self": "{source} tentou se restaurar com {keyword}, mas",
}

EFFECT_REMOVAL = {
    "burn": "{target} teve sua {removed_keyword} apagada pelo efeito de {keyword}.",
    "freeze": "{target} teve seu {removed_keyword} derretido pelo efeito de {keyword}.",
    "sleep": "{target} acordou de seu {removed_keyword} pelo efeito de {keyword}.",
}

FAILS = {
    "alive": "{target} estava vivo.",
    "alive_self": "estava vivo.",
    "dead": "{target} estava morto.",
    "dead_self": "estava morto.",
    "miss": "errou o alvo.",
    "miss_self": "se errou.",
}

KEYWORDS = {
    "absorb": "ABSORÇÃO",
    "attack": "ATACAR",
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
    "revive": "REVIVER",
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
