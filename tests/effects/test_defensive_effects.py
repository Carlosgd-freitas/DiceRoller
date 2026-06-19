"""Tests for defensive effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.sacred_block import SacredBlockEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager
    from src.combat.manager import CombatManager


def test_keyword_absorb(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    attack_effect_1 = AttackEffect(3)
    attack_effect_2 = AttackEffect(4)
    absorb_effect = AbsorbEffect(6)

    effect_manager.execute_effect(
        absorb_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
        monster_2.get_effect(Keyword.ABSORB).value == 6,
        monster_1.get_effect(Keyword.ABSORB) is None,
    ]

    effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 13,
            monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
            monster_2.get_effect(Keyword.ABSORB).value == 3,
        ]
    )

    effect_manager.execute_effect(
        attack_effect_2,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 15,
            monster_2.get_effect(Keyword.ABSORB) is None,
        ]
    )

    assert_conditions(conditions)


def test_keyword_block(managers: Dict):
    effect_manager: EffectManager = managers["effect_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    attack_effect_1 = AttackEffect(3)
    attack_effect_2 = AttackEffect(4)
    block_effect = BlockEffect(6)

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        monster_2.get_effect(Keyword.BLOCK).value == 6,
        monster_1.get_effect(Keyword.BLOCK) is None,
    ]

    effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_2.get_effect(Keyword.BLOCK).value == 3,
        ]
    )

    effect_manager.execute_effect(
        attack_effect_2,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 9,
            monster_2.get_effect(Keyword.BLOCK) is None,
        ]
    )

    assert_conditions(conditions)


def test_keyword_invulnerable(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    combat_manager.current_monster = monster_2

    attack_effect_1 = AttackEffect(1)
    attack_effect_99 = AttackEffect(99)
    invulnerable_effect = InvulnerableEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        invulnerable_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.INVULNERABLE).keyword == Keyword.INVULNERABLE,
        monster_2.get_effect(Keyword.INVULNERABLE).duration == 1,
        monster_1.get_effect(Keyword.INVULNERABLE) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.INVULNERABLE).keyword == Keyword.INVULNERABLE,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 9,
            monster_2.get_effect(Keyword.INVULNERABLE) is None,
        ]
    )

    assert_conditions(conditions)


def test_keyword_sacred_block(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    combat_manager.current_monster = monster_2

    attack_effect_1 = AttackEffect(1)
    attack_effect_99 = AttackEffect(99)
    sacred_block_effect = SacredBlockEffect(2)

    combat_manager.effect_manager.execute_effect(
        sacred_block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.SACRED_BLOCK).keyword == Keyword.SACRED_BLOCK,
        monster_2.get_effect(Keyword.SACRED_BLOCK).value == 2,
        monster_1.get_effect(Keyword.SACRED_BLOCK) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.SACRED_BLOCK).value == 1,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.SACRED_BLOCK) is None,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.local_id == "MONSTER_2",
            monster_2.hp == 9,
            monster_2.get_effect(Keyword.SACRED_BLOCK) is None,
        ]
    )

    assert_conditions(conditions)
