"""Tests for offensive effects processing."""

from src.base.side import Side
from src.base.effect import Effect
from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_attack(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side = Side(
        effects=[
            Effect(Keyword.ATTACK, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        len(targets) == 1,

        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert all(conditions)


def test_keyword_curse(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side = Side(
        effects=[
            Effect(Keyword.CURSE, 6),
        ]
    )

    targets = process_effect(
        side.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        len(targets) == 1,

        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 0,
        combat_manager.order[0].max_hp == 10,
    ]

    assert all(conditions)
