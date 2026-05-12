"""Tests for debuff effects processing."""

from src.base.side import Side
from src.base.dice import Dice
from src.base.keywords import Keyword
from src.effects.heal import HealEffect
from src.effects.burn import BurnEffect
from src.effects.stun import StunEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from tests.utils import assert_conditions
from src.effects.attack import AttackEffect
from src.effects.freeze import FreezeEffect
from src.effects.poison import PoisonEffect
from src.combat.manager import CombatManager


def test_keyword_bleed(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_bleed = BleedEffect(
        value=1,
        duration=1,
    )
    effect_attack_1 = AttackEffect(1)
    effect_attack_2 = AttackEffect(2)
    effect_attack_3 = AttackEffect(3)

    combat_manager.order[0].dice = [
        Dice(sides=[Side([effect_attack_1])]),
        Dice(sides=[Side([effect_attack_2])]),
        Dice(sides=[Side([effect_attack_3])]),
    ]

    combat_manager.order[0].add_effect(effect_bleed)

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

    rolled = combat_manager.roll(combat_manager.order[0])

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

    effect_blind = BlindEffect(
        value=1,
        duration=1,
    )
    effect_heal = HealEffect(2)
    effect_attack = AttackEffect(2)

    combat_manager.order[0].add_effect(effect_blind)

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

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend([
        combat_manager.order[0].hp == 7,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
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

    effect_burn = BurnEffect(
        value=2,
        duration=1,
    )

    combat_manager.order[0].add_effect(effect_burn)

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


def test_keyword_freeze(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_freeze = FreezeEffect(
        duration=1,
    )
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

    combat_manager.order[0].add_effect(effect_freeze)

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_0",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.FREEZE).keyword == Keyword.FREEZE,
        combat_manager.order[0].get_effect(Keyword.FREEZE).duration == 1,
        combat_manager.order[0].hp == 5,

        combat_manager.order[1].local_id == "MONSTER_1",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.FREEZE) == None,
        combat_manager.order[1].hp == 5,
    ]

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend([
        combat_manager.order[0].hp == 5,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.FREEZE) == None,
        combat_manager.order[0].hp == 7,

        combat_manager.order[1].hp == 3,
    ])

    assert_conditions(conditions)


def test_keyword_poison(effect_processing):
    combat_manager: CombatManager = effect_processing["combat_manager"]

    effect_poison = PoisonEffect(
        value=2,
        duration=1,
    )

    combat_manager.order[0].add_effect(effect_poison)

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

    effect_stun = StunEffect(
        duration=1,
    )
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

    combat_manager.order[0].add_effect(effect_stun)

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

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend([
        combat_manager.order[0].hp == 5,
        combat_manager.order[1].hp == 5,
    ])

    combat_manager.end_turn()

    effect_heal.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    effect_attack.activate(
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend([
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.STUN) == None,
        combat_manager.order[0].hp == 7,

        combat_manager.order[1].hp == 3,
    ])

    assert_conditions(conditions)
