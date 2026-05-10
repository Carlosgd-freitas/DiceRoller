"""Tests for debuff effects processing."""

from src.base.side import Side
from src.base.dice import Dice
from src.base.effect import Effect
from src.base.keywords import Keyword
from tests.utils import assert_conditions
from src.combat.manager import CombatManager
from src.processors.effects import process_effect


def test_keyword_bleed(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_bleed = Effect(
        Keyword.BLEED,
        value=1,
        duration=1,
    )
    effect_nothing_1 = Effect(Keyword.NOTHING, value=1)
    effect_nothing_2 = Effect(Keyword.NOTHING, value=2)
    effect_nothing_3 = Effect(Keyword.NOTHING, value=3)

    combat_manager.order[0].dice = [
        Dice(sides=[Side([effect_nothing_1])]),
        Dice(sides=[Side([effect_nothing_2])]),
        Dice(sides=[Side([effect_nothing_3])]),
    ]

    _ = process_effect(
        effect_bleed,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.BLEED).keyword == Keyword.BLEED,
        combat_manager.order[0].get_effect(Keyword.BLEED).value == 1,
        combat_manager.order[0].get_effect(Keyword.BLEED).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.BLEED) == None,
        combat_manager.order[1].hp == 5,
    ]

    rolled = combat_manager.order[0].roll()

    conditions.extend([
        len(rolled) == 3,
        rolled[0].effects[0].value == 1,
        rolled[1].effects[0].value == 2,
        rolled[2].effects[0].value == 3,

        combat_manager.order[0].hp == 2,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    rolled = combat_manager.order[0].roll()

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.BLEED) == None,

        combat_manager.order[0].hp == 2,
        combat_manager.order[1].hp == 5,
    ])

    assert_conditions(conditions)


def test_keyword_blind(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_blind = Effect(
        Keyword.BLIND,
        value=1,
        duration=1,
    )
    effect_attack = Effect(Keyword.ATTACK, 2)
    effect_heal = Effect(Keyword.HEAL, 2)

    _ = process_effect(
        effect_blind,
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
        effect_heal,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        effect_attack,
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        combat_manager.order[0].hp == 7,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    _ = process_effect(
        effect_heal,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        effect_attack,
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.BLIND) == None,
        combat_manager.order[0].hp == 9,

        combat_manager.order[1].hp == 3,
    ])

    assert_conditions(conditions)


def test_keyword_burn(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_burn = Effect(
        Keyword.BURN,
        value=2,
        duration=1,
    )

    _ = process_effect(
        effect_burn,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.BURN).keyword == Keyword.BURN,
        combat_manager.order[0].get_effect(Keyword.BURN).value == 2,
        combat_manager.order[0].get_effect(Keyword.BURN).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.BURN) == None,
        combat_manager.order[1].hp == 5,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.BURN) == None,

        combat_manager.order[0].hp == 3,
        combat_manager.order[1].hp == 5,
    ])

    assert_conditions(conditions)


def test_keyword_poison(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_poison = Effect(
        Keyword.POISON,
        value=2,
        duration=1,
    )

    _ = process_effect(
        effect_poison,
        source=combat_manager.order[1],
        targets=[combat_manager.order[0]],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.POISON).keyword == Keyword.POISON,
        combat_manager.order[0].get_effect(Keyword.POISON).value == 2,
        combat_manager.order[0].get_effect(Keyword.POISON).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.POISON) == None,
        combat_manager.order[1].hp == 5,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.POISON) == None,

        combat_manager.order[0].hp == 3,
        combat_manager.order[1].hp == 5,
    ])

    assert_conditions(conditions)


def test_keyword_stun(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_stun = Effect(
        Keyword.STUN,
        duration=1,
    )
    effect_attack = Effect(Keyword.ATTACK, 2)
    effect_heal = Effect(Keyword.HEAL, 2)

    _ = process_effect(
        effect_stun,
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
        effect_heal,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        effect_attack,
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        combat_manager.order[0].hp == 5,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    _ = process_effect(
        effect_heal,
        source=combat_manager.order[0],
        targets=[combat_manager.order[0]],
    )

    _ = process_effect(
        effect_attack,
        source=combat_manager.order[0],
        targets=[combat_manager.order[1]],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.STUN) == None,
        combat_manager.order[0].hp == 7,

        combat_manager.order[1].hp == 3,
    ])

    assert_conditions(conditions)
