"""PT-BR localization por effect types module."""

BUFF = {
    "name": "FORTALECIMENTO",
    "execution": "{source} fortaleceu {target} com {keyword} por {duration} turnos.",
    "execution_self": "{source} se fortaleceu com {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou fortalecer {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se fortalecer com {keyword}, mas",
}

CURSE = {
    "name": "MALDIÇÃO",
    "execution": "{source} amaldiçoou {target} com {keyword} por {duration} turnos.",
    "execution_self": "{source} se amaldiçoou com {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou amaldiçoar {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se amaldiçoar com {keyword}, mas",
}

DEBUFF = {
    "name": "ENFRAQUECIMENTO",
    "execution": "{source} enfraqueceu {target} com {keyword} por {duration} turnos.",
    "execution_self": "{source} se enfraqueceu com {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou enfraquecer {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se enfraquecer com {keyword}, mas",
}

DEFENSIVE = {
    "name": "DEFENSIVO",
    "execution": "{source} protegeu {target}. {target} recebeu {value} {keyword}.",
    "execution_self": "{source} se protegeu e recebeu {value} {keyword}.",
    "execution_fail": "{source} tentou proteger {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se proteger com {keyword}, mas",
}

DETERIORATION = {
    "name": "DETERIORAÇÃO",
    "execution": "{source} deteriorou {target} com {keyword} por {duration} turnos.",
    "execution_self": "{source} se deteriorou com {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou deteriorar {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se deteriorar com {keyword}, mas",
}

NOTHING = {
    "name": "NADA",
    "execution": "{source} não fez nada.",
    "execution_self": "{source} não fez nada.",
    "execution_fail": "{source} tentou não fazer nada, mas",
    "execution_fail_self": "{source} tentou não fazer nada, mas",
}

OFFENSIVE = {
    "name": "OFFENSIVO",
    "execution": "{source} {action} {target}.",
    "execution_self": "{source} se {action}.",
    "execution_fail": "{source} tentou {keyword} {target}, mas",
    "execution_fail_self": "{source} tentou se {keyword}, mas",
}

RESTORATION = {
    "name": "RESTAURAÇÃO",
    "execution": "{source} restaurou {target} com {keyword} por {duration} turnos.",
    "execution_self": "{source} se restaurou com {keyword} por {duration} turnos.",
    "execution_fail": "{source} tentou restaurar {target} com {keyword}, mas",
    "execution_fail_self": "{source} tentou se restaurar com {keyword}, mas",
}
