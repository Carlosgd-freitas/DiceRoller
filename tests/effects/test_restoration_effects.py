"""Tests for restoration effects processing."""

from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.regen import RegenEffect
from tests.utils import assert_conditions


def test_keyword_heal(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect = HealEffect(6)

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[1].hp == 7,
    ]

    assert_conditions(conditions)


def test_keyword_mana(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect = ManaEffect(2)

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_1",
        combat_manager.order[1].mana == 0,
    ]

    combat_manager.activate_effect(
        effect,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            combat_manager.order[1].mana == 2,
        ]
    )

    assert_conditions(conditions)


def test_keyword_mana_regen(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[2]

    effect = ManaRegenEffect(
        value=1,
        duration=1,
    )

    combat_manager.order[2].apply_effect(effect)

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        len(combat_manager.order[2].effects) == 1,
        combat_manager.order[2].get_effect(Keyword.MANA_REGEN).keyword
        == Keyword.MANA_REGEN,
        combat_manager.order[2].get_effect(Keyword.MANA_REGEN).value == 1,
        combat_manager.order[2].get_effect(Keyword.MANA_REGEN).duration == 1,
        combat_manager.order[2].mana == 0,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[2].effects) == 0,
            combat_manager.order[2].get_effect(Keyword.MANA_REGEN) is None,
            combat_manager.order[2].mana == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_regen(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[2]

    effect = RegenEffect(
        value=1,
        duration=1,
    )

    combat_manager.order[2].apply_effect(effect)

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        len(combat_manager.order[2].effects) == 1,
        combat_manager.order[2].get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        combat_manager.order[2].get_effect(Keyword.REGEN).value == 1,
        combat_manager.order[2].get_effect(Keyword.REGEN).duration == 1,
        combat_manager.order[2].hp == 10,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[2].effects) == 0,
            combat_manager.order[2].get_effect(Keyword.REGEN) is None,
            combat_manager.order[2].hp == 11,
        ]
    )

    assert_conditions(conditions)
