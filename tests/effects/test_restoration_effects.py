"""Tests for restoration effects processing."""

from src.base.keywords import Keyword
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.regen import RegenEffect
from tests.utils import assert_conditions
from src.combat.manager import CombatManager
from src.effects.mana_regen import ManaRegenEffect


def test_keyword_heal(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = HealEffect(6)

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )
    
    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        combat_manager.order[0].hp == 10,
        combat_manager.order[0].max_hp == 10,
    ]

    assert_conditions(conditions)


def test_keyword_mana(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = ManaEffect(2)

    mana_before = combat_manager.order[0].mana

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )
    
    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        mana_before == 0,
        combat_manager.order[0].mana == 2,
    ]

    assert_conditions(conditions)


def test_keyword_mana_regen(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = ManaRegenEffect(
        value=1,
        duration=1,
    )

    combat_manager.order[0].apply_effect(effect)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.MANA_REGEN).keyword == Keyword.MANA_REGEN,
        combat_manager.order[0].get_effect(Keyword.MANA_REGEN).value == 1,
        combat_manager.order[0].get_effect(Keyword.MANA_REGEN).duration == 1,
        combat_manager.order[0].mana == 0,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.MANA_REGEN) == None,

        combat_manager.order[0].mana == 1,
    ])

    assert_conditions(conditions)


def test_keyword_regen(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect = RegenEffect(
        value=1,
        duration=1,
    )

    combat_manager.order[0].apply_effect(effect)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        combat_manager.order[0].get_effect(Keyword.REGEN).value == 1,
        combat_manager.order[0].get_effect(Keyword.REGEN).duration == 1,
        combat_manager.order[0].hp == 5,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.REGEN) == None,

        combat_manager.order[0].hp == 6,
    ])

    assert_conditions(conditions)
