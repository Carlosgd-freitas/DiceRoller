"""PT-BR localization for effects module."""

ACTIONS = {
    "absorb": "ABSORVIDO",
    "attack": "ATACOU",
    "block": "BLOQUEADO",
    "doom": "CONDENOU",
    "drain": "DRENOU",
    "execute": "EXECUTOU",
    "invisible": "EVITADO",
    "pierce": "PERFUROU",
    "revive": "REVIVEU",
    "sacred_block": "SAGRADAMENTE BLOQUEADO",
}

ACTIVATION = {
    "bleed": "{target} recebeu {damage} de dano de {keyword}.",
    "burn": "{target} recebeu {damage} de dano de {keyword}.",
    "doom": "{target} foi morto pela {keyword}.",
    "doom_countdown": "Restam {duration} turnos para que {target} morra pela {keyword}.",
    "freeze": "{source} não pôde agir porque estava {status}.",
    "poison": "{target} recebeu {damage} de dano de {keyword}.",
    "mana_regen": "{target} restaurou {value} de {mana} de si mesmo através da {keyword}.",
    "regen": "{target} restaurou {value} de {hp} de si mesmo através da {keyword}.",
    "sleep": "{source} não pôde agir porque estava {status}.",
    "stun": "{source} não pôde agir porque estava {status}.",
    "thorns": "{target} recebeu {damage} de dano de {keyword}.",
}

DAMAGE = {
    # Part 1: Base message
    "base": "{source} {action} {target}.",
    "base_self": "{source} se {action}.",
    # Part 2: Defensive message
    "defended_damage": "{defended_damage} de dano foi {action}.",
    # Part 3: Damage message
    "damage": "{damage} de dano foi infligido.",
}

DESCRIPTION = {
    "absorb": "Reduz até {value} de dano direto recebido. Qualquer dano bloqueado restaura {hp}.",
    "attack": "Inflige {value} de dano.",
    "bleed": "Inflige {value} de dano toda vez que o alvo rola um dado.",
    "blind": "Diminui a acurácia dos dados e habilidades do alvo que não são usados em si mesmo em {value_perc}%.",
    "block": "Reduz até {value} de dano direto recebido.",
    "burn": "Inflige {value} de dano em todo início de turno. Remove {freeze}.",
    "cleanse": "Remove até {value} enfraquecimentos do alvo, começando pelo mais antigo.",
    "confuse": "Faz com que o alvo use seus dados e habilidades aleatoriamente.",
    "corrupt": "Remove até {value} fortalecimentos do alvo, começando pelo mais antigo.",
    "curse": "Inflige {value} de dano a si mesmo. Ignora efeitos defensivos.",
    "doom": "Mata o alvo após {duration} turnos.",
    "drain": "Inflige {value} de dano. Qualquer dano infligido restaura {hp}.",
    "execute": "Mata o alvo se seu {hp} for menor ou igul a {value_perc}% de seu {hp} máximo.",
    "focus": "Aumenta a acurácia dos dados e habilidades do alvo em {value_perc}%.",
    "freeze": "Impede que o alvo aja. Remove {burn}.",
    "heal": "Restaura {value} {hp}.",
    "immunity": "Faz com que o alvo seja imune a outros efeitos. Quaisquer efeitos que o alvo esteja sobre continuarão a ser aplicados.",
    "invisible": "Evita todo o dano direto recebido por {duration} turnos.",
    "mana_regen": "Aumenta {mana} em {value} em todo início de turno.",
    "mana": "Aumenta {mana} em {value}.",
    "nothing": "Não faz nada.",
    "pierce": "Inflige {value} de dano. Ignora {absorb}, {block} e {sacred_block}.",
    "poison": "Inflige {value} de dano em todo início de turno.",
    "regen": "Restaura {value} {hp} em todo início de turno.",
    "revive": "Revive um alvo morto e o cura em {value_perc}% de seu {hp} máximo.",
    "sacred_block": "Reduz todo o dano direto recebido até {value} vezes.",
    "sleep": "Impede que o alvo aja. Qualquer dano direto irá acordar o alvo.",
    "stun": "Impede que o alvo aja.",
    "thorns": "Quando atacado diretamente, inflige {value} de dano ao atacante.",
}

EXECUTION = {
    # Effect keywords
    "cleanse": "{source} removeu {count} enfraquecimentos de {target} através de {keyword}",
    "cleanse_self": "{source} removeu {count} enfraquecimentos de si mesmo através de {keyword}",
    "corrupt": "{source} removeu {count} fortalecimentos de {target} através de {keyword}",
    "corrupt_self": "{source} removeu {count} fortalecimentos de si mesmo através de {keyword}",
    "curse": "{source} infligiu {value} de dano em {target} através de {keyword}.",
    "curse_self": "{source} se infligiu {value} de dano através de {keyword}.",
    "doom": "{source} {action} {target}. {target} morrerá em {duration} turnos.",
    "doom_self": "{source} {action} a si mesmo. {source} morrerá em {duration} turnos.",
    "execute": "{source} {action} {target}.",
    "execute_self": "{source} se {action}.",
    "heal": "{source} restaurou {value} de {hp} de {target} através de {keyword}.",
    "heal_self": "{source} restaurou {value} de {hp} de si mesmo através de {keyword}.",
    "immunity": "{source} concedeu {keyword} de {count} efeitos a {target}",
    "immunity_self": "{source} concedeu {keyword} de {count} efeitos a si mesmo",
    "invisible": "{source} tornou {target} {keyword} por {duration} turnos.",
    "invisible_self": "{source} se tornou {keyword} por {duration} turnos.",
    "mana": "{source} restaurou {value} de {mana} de {target} através de {keyword}.",
    "mana_self": "{source} restaurou {value} de {mana} de si mesmo através de {keyword}.",
    "revive": "{source} {action} {target}. {target} foi curado em {value_perc}% de seu {hp} máximo.",
    "revive_self": "{source} {action} a si mesmo e se curou em {value_perc}% de seu {hp} máximo.",
    # Effect types
    "buff": "{source} fortaleceu {target} com {keyword} por {duration} turnos.",
    "buff_self": "{source} se fortaleceu com {keyword} por {duration} turnos.",
    "debuff": "{source} enfraqueceu {target} com {keyword} por {duration} turnos.",
    "debuff_self": "{source} se enfraqueceu com {keyword} por {duration} turnos.",
    "defensive": "{source} protegeu {target}. {target} recebeu {value} de {keyword}.",
    "defensive_self": "{source} se protegeu e recebeu {value} de {keyword}.",
    "nothing": "Nada aconteceu.",
    "nothing_self": "Nada aconteceu.",
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
    "freeze": "{target} estava {status}.",
    "freeze_self": "estava {status}.",
    "immunity": "{target} era {status}.",
    "immunity_self": "era {status}",
    "miss": "errou o alvo.",
    "miss_self": "se errou.",
    "sleep": "{target} estava {status}.",
    "sleep_self": "estava {status}.",
    "stun": "{target} estava {status}.",
    "stun_self": "estava {status}.",
}

KEYWORDS = {
    "absorb": "ABSORÇÃO",
    "attack": "ATACAR",
    "bleed": "SANGRAMENTO",
    "blind": "CEGUEIRA",
    "block": "BLOQUEIO",
    "burn": "QUEIMADURA",
    "cleanse": "PURIFICAR",
    "confuse": "CONFUSÃO",
    "corrupt": "CORROMPER",
    "curse": "MALDIÇÃO",
    "doom": "CONDENAÇÃO",
    "drain": "DRENAR",
    "execute": "EXECUTAR",
    "focus": "FOCO",
    "freeze": "CONGELAMENTO",
    "heal": "CURA",
    "immunity": "IMUNIDADE",
    "invisible": "INVISÍVEL",
    "mana_regen": "REGENERAÇÃO DE MANA",
    "mana": "MANA",
    "nothing": "NADA",
    "pierce": "PERFURAR",
    "poison": "ENVENENAMENTO",
    "regen": "REGENERAÇÃO",
    "revive": "REVIVER",
    "sacred_block": "BLOQUEIO SAGRADO",
    "sleep": "SONO",
    "stun": "ATORDOAMENTO",
    "thorns": "ESPINHOS",
}

REMOVAL = {
    "blind": "{target} teve sua {removed_keyword} curada pelo efeito de {keyword}.",
    "burn": "{target} teve sua {removed_keyword} apagada pelo efeito de {keyword}.",
    "focus": "{target} teve seu {removed_keyword} perturbado pelo efeito de {keyword}.",
    "freeze": "{target} teve seu {removed_keyword} derretido pelo efeito de {keyword}.",
    "sleep": "{target} acordou de seu {removed_keyword} pelo efeito de {keyword}.",
}

STATUS = {
    "blind": "CEGO",
    "confuse": "CONFUSO",
    "doom": "CONDENADO",
    "freeze": "CONGELADO",
    "immunity": "IMUNE",
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
