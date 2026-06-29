"""PT-BR localization for effects module."""

ABSORB = {
    "name": "ABSORÇÃO",
    "description": "Reduz até {value} de dano direto recebido. Qualquer dano bloqueado restaura {hp}.",
    "action": "ABSORVIDO",
    "activation": "{defended_damage} de dano foi {defensive_action}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "ABSORVENDO",
}

ATTACK = {
    "name": "ATACAR",
    "description": "Inflige {value} de dano.",
    "action": "ATACOU",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} se {action}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

BLEED = {
    "name": "SANGRAMENTO",
    "description": "Inflige {value} de dano toda vez que o alvo rola um dado.",
    "action": None,
    "activation": "{target} recebeu {damage} de dano de {keyword}.",
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
    "name": "CEGUEIRA",
    "description": "Diminui a acurácia dos dados e habilidades que o alvo não usa m si mesmo em {value_perc}%.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} teve sua {removed_keyword} curada pelo efeito de {keyword}.",
    "status": "CEGO",
}

BLOCK = {
    "name": "BLOQUEIO",
    "description": "Reduz até {value} de dano direto recebido.",
    "action": "BLOQUEADO",
    "activation": "{defended_damage} de dano foi {defensive_action}.",
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
    "name": "QUEIMADURA",
    "description": "Inflige {value} de dano em todo início de turno. Remove {freeze}.",
    "action": None,
    "activation": "{target} recebeu {damage} de dano de {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} teve sua {removed_keyword} apagada pelo efeito de {keyword}.",
    "status": "QUEIMANDO",
}

CLEANSE = {
    "name": "PURIFICAR",
    "description": "Remove até {value} enfraquecimentos do alvo, começando pelo mais antigo.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} removeu {count} enfraquecimentos de {target} através de {keyword}",
    "execution_self": "{source} removeu {count} enfraquecimentos de si mesmo através de {keyword}",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

CONFUSE = {
    "name": "CONFUSÃO",
    "description": "Faz com que o alvo use seus dados e habilidades aleatoriamente.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "CONFUSO",
}

CORRUPT = {
    "name": "CORROMPER",
    "description": "Remove até {value} fortalecimentos do alvo, começando pelo mais antigo.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} removeu {count} fortalecimentos de {target} através de {keyword}",
    "execution_self": "{source} removeu {count} fortalecimentos de si mesmo através de {keyword}",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

DOOM = {
    "name": "CONDENAÇÃO",
    "description": "Mata o alvo após {duration} turnos.",
    "action": "CONDENOU",
    "activation": "{target} foi morto pela {keyword}.",
    "countdown": "Restam {duration} turnos para que {target} morra pela {keyword}.",
    "execution": "{source} {action} {target}. {target} morrerá em {duration} turnos.",
    "execution_self": "{source} {action} a si mesmo. {source} morrerá em {duration} turnos.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "CONDENADO",
}

DRAIN = {
    "name": "DRENAR",
    "description": "Inflige {value} de dano. Qualquer dano infligido restaura {hp}.",
    "action": "DRENOU",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} se {action}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

EXECUTE = {
    "name": "EXECUTAR",
    "description": "Mata o alvo se seu {hp} for menor ou igul a {value_perc}% de seu {hp} máximo.",
    "action": "EXECUTOU",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} se {action}.",
    "execution_fail": "{source} tentou {keyword} {target}, mas",
    "execution_fail_self": "{source} tentou se {keyword}, mas",
    "fail": None,
    "removal": None,
    "status": None,
}

FOCUS = {
    "name": "FOCO",
    "description": "Aumenta a acurácia dos dados e habilidades do alvo em {value_perc}%.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} teve seu {removed_keyword} perturbado pelo efeito de {keyword}.",
    "status": None,
}

FORTIFY = {
    "name": "FORTIFICAR",
    "description": "Aumenta a redução de dano de efeitos defensivos em {value}.",
    "action": "FORTIFICAR",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "FORTIFICADO",
}

FRAGILE = {
    "name": "FRÁGIL",
    "description": "Reduz a redução de dano de efeitos defensivos em {value}.",
    "action": "FRAGILIZAR",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "FRÁGIL",
}

FREEZE = {
    "name": "CONGELAMENTO",
    "description": "Impede que o alvo aja. Remove {burn}.",
    "action": None,
    "activation": "{source} não pôde agir porque estava {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} estava {status}.",
    "removal": "{target} teve seu {removed_keyword} derretido pelo efeito de {keyword}.",
    "status": "CONGELADO",
}

FROSTBURN = {
    "name": "QUEIMADURA FRIA",
    "description": "Inflige {value} de dano em todo início de turno.",
    "action": None,
    "activation": "{target} recebeu {damage} de dano de {keyword}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": "QUEIMANDO DE FRIO",
}

HASTE = {
    "name": "ACELERAÇÃO",
    "description": "Aumenta a velocidade do alvo em {value}.",
    "action": "ACELERAR",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "ACELERADO",
}

HEAL = {
    "name": "CURA",
    "description": "Restaura {value} {hp}.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} restaurou {value} de {hp} de {target} através de {keyword}.",
    "execution_self": "{source} restaurou {value} de {hp} de si mesmo através de {keyword}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

IMMUNITY = {
    "name": "IMUNIDADE",
    "description": "Faz com que o alvo seja imune a outros efeitos. Quaisquer efeitos que o alvo esteja sobre continuarão a ser aplicados.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} concedeu {keyword} de {count} efeitos a {target}",
    "execution_self": "{source} concedeu {keyword} de {count} efeitos a si mesmo",
    "execution_fail": "{source} tentou tornar {target} {status}, mas",
    "execution_fail_self": "{source} tentou se tornar {status}, mas",
    "fail": "{target} era {status}.",
    "removal": None,
    "status": "IMUNE",
}

INVISIBLE = {
    "name": "INVISÍVEL",
    "description": "Faz o alvo inalvejável pelos inimigos.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} tornou {target} {keyword} por {duration} turnos.",
    "execution_self": "{source} se tornou {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou tornar {target} {keyword}, mas",
    "execution_fail_self": "{source} tentou se tornar {keyword}, mas",
    "fail": None,
    "removal": None,
    "status": None,
}

INVULNERABLE = {
    "name": "INVULNERÁVEL",
    "description": "Nega qualquer dano que seria infligido ao {hp} do alvo.",
    "action": None,
    "activation": "{defended_damage} de dano foi negado porque {target} estava {defensive_status}.",
    "countdown": None,
    "execution": "{source} tornou {target} {keyword} por {duration} turnos.",
    "execution_self": "{source} se tornou {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou tornar {target} {keyword}, mas",
    "execution_fail_self": "{source} tentou se tornar {keyword}, mas",
    "fail": None,
    "removal": None,
    "status": "INVULNERÁVEL",
}

MANA_REGEN = {
    "name": "REGENERAÇÃO DE MANA",
    "description": "Aumenta {mana} em {value} em todo início de turno.",
    "action": None,
    "activation": "{target} restaurou {value} de {mana} de si mesmo através da {keyword}.",
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
    "description": "Aumenta {mana} em {value}.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} restaurou {value} de {mana} de {target} através de {keyword}.",
    "execution_self": "{source} restaurou {value} de {mana} de si mesmo através de {keyword}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

NOTHING = {
    "name": "NADA",
    "description": "Não faz nada.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "Nada aconteceu.",
    "execution_self": "Nada aconteceu.",
    "execution_fail": "Nada aconteceria, mas {source}",
    "execution_fail_self": "Nada aconteceria, mas {source}",
    "fail": None,
    "removal": None,
    "status": None,
}

OIL = {
    "name": "ÓLEO",
    "description": "Reduz a velocidade do alvo e aumenta o dano infligido por {burn} em {value}.",
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
    "name": "DOR",
    "description": "Inflige {value} de dano a si mesmo. Ignora efeitos defensivos.",
    "action": None,
    "activation": None,
    "countdown": None,
    "execution": "{source} infligiu {value} de dano em {target} através de {keyword}.",
    "execution_self": "{source} se infligiu {value} de dano através de {keyword}.",
    "execution_fail": "{source} iria causar {keyword} em {target}, mas",
    "execution_fail_self": "{source} iria sentir {keyword}, mas",
    "fail": None,
    "removal": None,
    "status": None,
}

PIERCE = {
    "name": "PERFURAR",
    "description": "Inflige {value} de dano. Ignora {absorb}, {block} e {sacred_block}.",
    "action": "PERFUROU",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} se {action}.",
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": None,
    "status": None,
}

POISON = {
    "name": "VENENO",
    "description": "Inflige {value} de dano em todo início de turno.",
    "action": None,
    "activation": "{target} recebeu {damage} de dano de {keyword}.",
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
    "name": "REGENERAÇÃO",
    "description": "Restaura {value} {hp} em todo início de turno.",
    "action": None,
    "activation": "{target} restaurou {value} de {hp} de si mesmo através da {keyword}.",
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
    "name": "REPELIR",
    "description": "Diminui a prioridade do alvo para os inimigos.",
    "action": "REPELIU",
    "activation": None,
    "countdown": None,
    "execution": "{source} fez {target} {keyword} os inimigos por {duration} turnos.",
    "execution_self": "{source} {action} os inimigos por {duration} turnos.",
    "execution_fail": "{source} tentou fazer {target} {keyword} os inimigos, mas",
    "execution_fail_self": "{source} tentou {keyword} os inimigos, mas",
    "fail": None,
    "removal": "{target} parou de {removed_keyword} pelo efeito de {keyword}.",
    "status": "REPELINDO",
}

REVIVE = {
    "name": "REVIVER",
    "description": "Revive um alvo morto e o cura em {value_perc}% de seu {hp} máximo.",
    "action": "REVIVEU",
    "activation": None,
    "countdown": None,
    "execution": "{source} {action} {target}. {target} foi curado em {value_perc}% de seu {hp} máximo.",
    "execution_self": "{source} {action} a si mesmo e se curou em {value_perc}% de seu {hp} máximo.",
    "execution_fail": "{source} tentou {keyword} {target}, mas",
    "execution_fail_self": "{source} tentou se {keyword}, mas",
    "fail": None,
    "removal": None,
    "status": None,
}

SACRED_BLOCK = {
    "name": "BLOQUEIO SAGRADO",
    "description": "Reduz todo o dano direto recebido até {value} vezes.",
    "action": "SAGRADAMENTE BLOQUEADO",
    "activation": "{defended_damage} de dano foi {defensive_action}.",
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
    "name": "SONO",
    "description": "Impede que o alvo aja. Qualquer dano direto irá acordar o alvo.",
    "action": None,
    "activation": "{source} não pôde agir porque estava {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} estava {status}.",
    "removal": "{target} acordou de seu {removed_keyword} pelo efeito de {keyword}.",
    "status": "DORMINDO",
}

SLOW = {
    "name": "LENTIDÃO",
    "description": "Reduz a velocidade do alvo em {value}.",
    "action": "DESACELEROU",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "LENTO",
}

STRENGTH = {
    "name": "FORÇA",
    "description": "Aumenta o dano infligido por efeitos ofensivos em {value}.",
    "action": "FORTALECER",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "FORTE",
}

STUN = {
    "name": "ATORDOAMENTO",
    "description": "Impede que o alvo aja.",
    "action": None,
    "activation": "{source} não pôde agir porque estava {status}.",
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": "{target} estava {status}.",
    "removal": None,
    "status": "ATORDOADO",
}

TAUNT = {
    "name": "PROVOCAR",
    "description": "Aumenta a prioridade do alvo para os inimigos.",
    "action": "PROVOCOU",
    "activation": None,
    "countdown": None,
    "execution": "{source} fez {target} {keyword} os inimigos por {duration} turnos.",
    "execution_self": "{source} {action} os inimigos por {duration} turnos.",
    "execution_fail": "{source} tentou fazer {target} {keyword} os inimigos, mas",
    "execution_fail_self": "{source} tentou {keyword} os inimigos, mas",
    "fail": None,
    "removal": "{target} parou de {removed_keyword} pelo efeito de {keyword}.",
    "status": "PROVOCANDO",
}

THORNS = {
    "name": "ESPINHOS",
    "description": "Quando atacado diretamente, inflige {value} de dano ao atacante.",
    "action": None,
    "activation": "{target} recebeu {damage} de dano de {keyword}.",
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
    "name": "FRAQUEZA",
    "description": "Reduz o dano infligido por efeitos ofensivos em {value}.",
    "action": "ENFRAQUECER",
    "activation": None,
    "countdown": None,
    "execution": None,
    "execution_self": None,
    "execution_fail": None,
    "execution_fail_self": None,
    "fail": None,
    "removal": "{target} não está mais {removed_status} pelo efeito de {keyword}.",
    "status": "FRACO",
}
