"""PT-BR localization for combat module."""

ACTIONS = {
    "roll_dice": "{name} rolou seus dados e tirou:",
    "skip_turn": "{name} decidiu não fazer nada.",
}

COMBAT = {
    "ai": "IA",
    "damage": "{damage} de dano foi infligido.",
    "died": "morreu",
    "draw": "É um empate!",
    "player": "JOGADOR",
    "round": "Rodada",
    "team": "Time",
    "turn": "Turno",
    "winner": "\nO time {team_name} é o vencedor!",
}

FAILS = {
    "act_disabled": "não pôde agir.",
    "default": "falhou.",
    "non-persistable": "foi ineficaz.",
    "source_alive": "estava vivo.",
    "source_dead": "morreu antes de poder fazer isso.",
    "source_freeze": "estava {fail_status}.",
    "source_immunity": "era {fail_status}.",
    "source_miss": "se errou.",
    "source_sleep": "estava {fail_status}.",
    "source_stun": "estava {fail_status}.",
    "target_alive": "{target} estava vivo.",
    "target_dead": "{target} estava morto.",
    "target_freeze": "{target} estava {fail_status}.",
    "target_immunity": "{target} era {fail_status}",
    "target_miss": "errou o alvo.",
    "target_sleep": "{target} estava {fail_status}.",
    "target_stun": "{target} estava {fail_status}.",
}

ORDER = {
    "faster": "MAIS RÁPIDO",
    "order": "Ordem de Combate",
    "sequential": "SEQUENCIAL",
    "shuffle": "EMBARALHADO",
    "slower": "MAIS LENTO",
}
