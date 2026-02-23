"""Tests for debuff effects processing."""

from src.base.side import Side
from src.base.effect import Effect
from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_blind(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side_blind = Side(
        effects=[
            Effect(
                Keyword.BLIND,
                value=1,
                duration=1,
            ),
        ]
    )
    side_attack = Side(
        effects=[
            Effect(Keyword.ATTACK, 2),
        ]
    )
    side_heal = Side(
        effects=[
            Effect(Keyword.HEAL, 2),
        ]
    )

    _ = process_effect(
        side_blind.effects[0],
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
        combat_manager.order[0].get_effect(Keyword.BLIND).value == 1,
        combat_manager.order[0].get_effect(Keyword.BLIND).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.BLIND) == None,
        combat_manager.order[1].hp == 5,
    ]

    _ = process_effect(
        side_heal.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        side_attack.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        combat_manager.order[0].hp == 7,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    _ = process_effect(
        side_heal.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        side_attack.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.BLIND) == None,
        combat_manager.order[0].hp == 9,

        combat_manager.order[1].hp == 3,
    ])

    assert all(conditions)


def test_keyword_stun(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    side_stun = Side(
        effects=[
            Effect(
                Keyword.STUN,
                duration=1,
            ),
        ]
    )
    side_attack = Side(
        effects=[
            Effect(Keyword.ATTACK, 2),
        ]
    )
    side_heal = Side(
        effects=[
            Effect(Keyword.HEAL, 2),
        ]
    )

    _ = process_effect(
        side_stun.effects[0],
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.STUN).keyword == Keyword.STUN,
        combat_manager.order[0].get_effect(Keyword.STUN).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.STUN) == None,
        combat_manager.order[1].hp == 5,
    ]

    _ = process_effect(
        side_heal.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        side_attack.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        combat_manager.order[0].hp == 5,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    _ = process_effect(
        side_heal.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        side_attack.effects[0],
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.STUN) == None,
        combat_manager.order[0].hp == 7,

        combat_manager.order[1].hp == 3,
    ])

    assert all(conditions)
