"""PT-BR localization for combat module."""

ACTIONS = {
    "roll_dice": "{name} rolou seus dados e tirou:",
    "skill": "{monster_name} usou {skill_name} e tirou:",
    "consumable": "{monster_name} usou {consumable_name} e tirou:",
    "skip_turn": "{name} decidiu não fazer nada.",
    "no_roll_dice": "{name} não tem dados pra rolar.",
    "no_skills": "{name} não pode usar nenhuma habilidade.",
    "no_consumables": "Não há consumíveis que {name} possa usar.",
    "no_equipment": "Não há equipamentos para {name}.",
    "no_show_details": "{name} não consegue ver os detalhes de nada!",
    "no_skip_turn": "{name} tem que fazer alguma coisa!",
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
    "delay": "nenhum efeito pôde ser extendido.",
    "non-persistable": "foi ineficaz.",
    "source_alive": "estava vivo.",
    "source_dead": "morreu antes de poder fazer isso.",
    "source_freeze": "estava {fail_status}.",
    "source_immunity": "era {fail_status}.",
    "source_miss": "se errou.",
    "source_resistance": "{fail_action}.",
    "source_sleep": "estava {fail_status}.",
    "source_stun": "estava {fail_status}.",
    "target_alive": "{target} estava vivo.",
    "target_dead": "{target} estava morto.",
    "target_freeze": "{target} estava {fail_status}.",
    "target_immunity": "{target} era {fail_status}",
    "target_miss": "errou o alvo.",
    "target_resistance": "{target} {fail_action}.",
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
