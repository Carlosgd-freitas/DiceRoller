"""Tests for defensive effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.pierce import PierceEffect
from src.effects.sacred_block import SacredBlockEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager
    from src.combat.manager import CombatManager


def test_absorb_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    attack_effect_1 = AttackEffect(Stat(flat=3))
    attack_effect_2 = AttackEffect(Stat(flat=20))
    absorb_effect = AbsorbEffect(Stat(flat=6))

    effect_manager.execute_effect(
        absorb_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        monster_1.get_effect(Keyword.ABSORB) is None,
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
        monster_2.get_effect(Keyword.ABSORB).value == Stat(flat=6),
    ]

    effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 13,
            monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
            monster_2.get_effect(Keyword.ABSORB).value == Stat(flat=3),
        ]
    )

    absorb_effect = AbsorbEffect(Stat(percent=0.1))

    effect_manager.execute_effect(
        absorb_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 13,
            monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
            monster_2.get_effect(Keyword.ABSORB).value == Stat(flat=18, percent=None),
        ]
    )

    effect_manager.execute_effect(
        attack_effect_2,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 29,
            monster_2.get_effect(Keyword.ABSORB) is None,
        ]
    )

    absorb_effect = AbsorbEffect(Stat(flat=1, percent=0.1))

    effect_manager.execute_effect(
        absorb_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.get_effect(Keyword.ABSORB).keyword == Keyword.ABSORB,
            monster_2.get_effect(Keyword.ABSORB).value == Stat(flat=16, percent=None),
        ]
    )

    assert_conditions(conditions)


def test_block_effect(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    attack_effect_1 = AttackEffect(Stat(flat=3))
    attack_effect_2 = AttackEffect(Stat(flat=20))
    block_effect = BlockEffect(Stat(flat=6))

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        monster_1.get_effect(Keyword.BLOCK) is None,
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
        monster_2.get_effect(Keyword.BLOCK).value == Stat(flat=6),
    ]

    effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_2.get_effect(Keyword.BLOCK).value == Stat(flat=3),
        ]
    )

    block_effect = BlockEffect(Stat(percent=0.1))

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_2.get_effect(Keyword.BLOCK).value == Stat(flat=18, percent=None),
        ]
    )

    effect_manager.execute_effect(
        attack_effect_2,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 8,
            monster_2.get_effect(Keyword.BLOCK) is None,
        ]
    )

    block_effect = BlockEffect(Stat(flat=1, percent=0.1))

    effect_manager.execute_effect(
        block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_2.get_effect(Keyword.BLOCK).value == Stat(flat=16, percent=None),
        ]
    )

    assert_conditions(conditions)


def test_invulnerable_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.current_monster = monster_2

    attack_effect_1 = AttackEffect(Stat(flat=1))
    attack_effect_99 = AttackEffect(Stat(flat=99))
    pierce_effect = PierceEffect(Stat(flat=1))
    invulnerable_effect = InvulnerableEffect(target_keywords=[Keyword.ALL], duration=1)

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

    combat_manager.effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.INVULNERABLE).keyword == Keyword.INVULNERABLE,
        ]
    )

    combat_manager.end_turn()

    combat_manager.current_monster = monster_2

    invulnerable_effect = InvulnerableEffect(
        target_keywords=[Keyword.ATTACK], duration=1
    )

    combat_manager.effect_manager.execute_effect(
        invulnerable_effect,
        source=monster_2,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_2.hp == 9,
            monster_2.get_effect(Keyword.INVULNERABLE) is None,
        ]
    )

    invulnerable_effect = InvulnerableEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        attack_effect_1,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        pierce_effect,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_2.hp == 7,
            monster_2.get_effect(Keyword.INVULNERABLE) is None,
        ]
    )

    assert_conditions(conditions)


def test_sacred_block_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.current_monster = monster_2

    attack_effect_1 = AttackEffect(Stat(flat=1))
    attack_effect_99 = AttackEffect(Stat(flat=99))
    sacred_block_effect = SacredBlockEffect(Stat(flat=2))

    combat_manager.effect_manager.execute_effect(
        sacred_block_effect,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        monster_2.hp == 10,
        monster_2.get_effect(Keyword.SACRED_BLOCK).keyword == Keyword.SACRED_BLOCK,
        monster_2.get_effect(Keyword.SACRED_BLOCK).value == Stat(flat=2),
        monster_1.get_effect(Keyword.SACRED_BLOCK) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_2.get_effect(Keyword.SACRED_BLOCK).value == Stat(flat=1),
        ]
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect_99,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
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
            monster_2.hp == 9,
            monster_2.get_effect(Keyword.SACRED_BLOCK) is None,
        ]
    )

    assert_conditions(conditions)
