"""Tests for restoration effects processing."""

from src.base.side import Side
from src.base.effect import Effect
from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_heal(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side = Side(
        effects=[
            Effect(Keyword.HEAL, 6),
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
        combat_manager.order[0].hp == 10,
        combat_manager.order[0].max_hp == 10,
    ]

    assert all(conditions)


def test_keyword_mana(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side = Side(
        effects=[
            Effect(Keyword.MANA, 2),
        ]
    )

    mana_before = combat_manager.order[0].mana

    targets = process_effect(
        side.effects[0],
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )
    
    conditions = [
        len(targets) == 1,

        combat_manager.order[0].local_id == "MONSTER_0",
        mana_before == 0,
        combat_manager.order[0].mana == 2,
    ]

    assert all(conditions)
