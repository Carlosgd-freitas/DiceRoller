"""PT-BR localization for effects module."""

ACTIONS = {
    "absorb": "ABSORVIDO",
    "attack": "ATACOU",
    "block": "BLOQUEADO",
    "drain": "DRENOU",
    "execute": "EXECUTOU",
    "invisible": "EVITADO",
    "pierce": "PERFUROU",
    "revive": "REVIVEU",
}

ACTIVATION = {
    "bleed": "{target} recebeu {damage} de dano de {keyword}.",
    "burn": "{target} recebeu {damage} de dano de {keyword}.",
    "doom": "{target} encontrou seu fim pela {keyword}.",
    "freeze": "{target} não pôde agir porque estava {status}.",
    "poison": "{target} recebeu {damage} de dano de {keyword}.",
    "mana_regen": "{target} restaurou {value} de {attribute} de si mesmo através da {keyword}.",
    "regen": "{target} restaurou {value} de {attribute} de si mesmo através da {keyword}.",
    "sleep": "{target} não pôde agir porque estava {status}.",
    "stun": "{target} não pôde agir porque estava {status}.",
    "thorns": "{target} recebeu {damage} de dano de {keyword}.",
}

COMPENDIUM = {
    "item_not_found": "Efeito não foi encontrado.",
    "next_item": "Próximo Efeito",
    "previous_item": "Efeito Anterior",
    "search_prompt": "Digite o nome de um efeito",
    "select_item_prompt": "Selecione um efeito (ou [0] para cancelar)",
    "title": "Compêndio de Efeitos",
}

DAMAGE = {
    # Part 1: Base message
    "base": "{source} {action} {target}.",
    "base_self": "{source} se {action}.",
    # Part 2: Defensive messages
    "absorb": "{absorbed_damage} de dano foi {action}.",
    "block": "{blocked_damage} de dano foi {action}.",
    "invisible": "{avoided_damage} de dano foi {action}.",
    # Part 3: Damage message
    "damage": "{damage} de dano foi infligido.",
}

DESCRIPTION = {
    "absorb": "Reduz até {value} de dano direto recebido. Qualquer dano bloqueado restaura {hp}.",
    "attack": "Inflige {value} de dano.",
    "bleed": "Inflige {value} de dano toda vez que o alvo rola um dado.",
    "blind": "Aumenta a chance de erro dos dados e habilidades do alvo em {value_perc}%.",
    "block": "Reduz até {value} de dano direto recebido.",
    "burn": "Inflige {value} de dano em todo início de turno. Remove {freeze}.",
    "confuse": "Faz com que o alvo use seus dados e habilidades aleatoriamente.",
    "curse": "Inflige {value} de dano a si mesmo. Ignora efeitos defensivos.",
    "doom": "Mata o alvo após {duration} turnos.",
    "drain": "Inflige {value} de dano. Qualquer dano infligido restaura {hp}.",
    "execute": "Mata o alvo se seu {hp} for menor ou igul a {value_perc}% de seu {hp} máximo.",
    "freeze": "Impede que o alvo aja. Remove {burn}.",
    "heal": "Restaura {value} {hp}.",
    "invisible": "Evita todo o dano direto recebido por {duration} turnos.",
    "mana_regen": "Aumenta {mana} em {value} em todo início de turno.",
    "mana": "Aumenta {mana} em {value}.",
    "nothing": "Não faz nada.",
    "pierce": "Inflige {value} de dano. Ignora efeitos defensivos.",
    "poison": "Inflige {value} de dano em todo início de turno.",
    "regen": "Restaura {value} {hp} em todo início de turno.",
    "revive": "Revive um alvo morto e o cura em {value_perc}% de seu {hp} máximo.",
    "sleep": "Impede que o alvo aja. Qualquer dano direto irá acordar o alvo.",
    "stun": "Impede que o alvo aja.",
    "thorns": "Quando atacado diretamente, inflige {value} de dano ao atacante.",
}

EXECUTION = {
    # Effect keywords
    "execute": "{source} {action} {target}.",
    "execute_self": "{source} se {action}.",
    "invisible": "{source} tornou {target} {keyword} por {duration} turnos.",
    "invisible_self": "{source} se tornou {keyword} por {duration} turnos.",
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

EXECUTION_FAIL = {
    # Effect keywords
    "execute": "{source} tentou {keyword} {target}, mas",
    "execute_self": "{source} tentou se {keyword}, mas",
    "invisible": "{source} tentou tornar {target} {keyword}, mas",
    "invisible_self": "{source} tentou se tornar {keyword}, mas",
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

FAILS = {
    "alive": "{target} estava vivo.",
    "alive_self": "estava vivo.",
    "dead": "{target} estava morto.",
    "dead_self": "estava morto.",
    "default": "falhou.",
    "default_self": "falhou.",
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
    "doom": "CONDENAÇÃO",
    "drain": "DRENAR",
    "execute": "EXECUTAR",
    "freeze": "CONGELAMENTO",
    "heal": "CURA",
    "invisible": "INVISÍVEL",
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

REMOVAL = {
    "burn": "{target} teve sua {removed_keyword} apagada pelo efeito de {keyword}.",
    "freeze": "{target} teve seu {removed_keyword} derretido pelo efeito de {keyword}.",
    "sleep": "{target} acordou de seu {removed_keyword} pelo efeito de {keyword}.",
}

STATUS = {
    "blind": "CEGO",
    "confuse": "CONFUSO",
    "freeze": "CONGELADO",
    "sleep": "DORMINDO",
    "stun": "ATORDOADO",
}

TYPES = {
    "buff": "FORTALECIMENTO",
    "debuff": "ENFRAQUECIMENTO",
    "defensive": "DEFENSIVO",
    "deterioration": "DETERIORAÇÃO",
    "nothing": "NADA",
    "offensive": "OFFENSIVO",
    "restoration": "RESTAURAÇÃO",
}
