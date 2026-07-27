"""Tests for damage procesing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from src.base.keywords import Keyword
from src.base.stat import Stat
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.sacred_block import SacredBlockEffect
from src.processors.damage import calculate_damage
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.effects import EffectManager


def test_calculate_damage_no_consider(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[],
    )

    conditions = [
        damage_data["damage"] == 6,
        damage_data["defended_damage"] == {},
    ]

    assert_conditions(conditions)


def test_calculate_damage_over(combat: Dict):
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    effect = AttackEffect(Stat(flat=300))

    damage_data = calculate_damage(
        effect,
        monster_0,
        monster_4,
    )

    conditions = [
        damage_data["damage"] == 200,
        damage_data["defended_damage"] == {},
    ]

    assert_conditions(conditions)


def test_calculate_damage_block(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))
    block_effect = BlockEffect(Stat(flat=1))

    effect_manager.execute_effect(
        block_effect,
        monster_4,
        monster_4,
    )

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[Keyword.BLOCK],
    )

    conditions = [
        damage_data["damage"] == 5,
        len(damage_data["defended_damage"]) == 2,
        damage_data["defended_damage"]["block"] == 1,
        damage_data["defended_damage"]["total"] == 1,
    ]

    assert_conditions(conditions)


def test_calculate_damage_absorb(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))
    absorb_effect = AbsorbEffect(Stat(flat=2))

    effect_manager.execute_effect(
        absorb_effect,
        monster_4,
        monster_4,
    )

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[Keyword.ABSORB],
    )

    conditions = [
        damage_data["damage"] == 4,
        len(damage_data["defended_damage"]) == 2,
        damage_data["defended_damage"]["absorb"] == 2,
        damage_data["defended_damage"]["total"] == 2,
    ]

    assert_conditions(conditions)


def test_calculate_damage_sacred_block(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))
    sacred_block_effect = SacredBlockEffect(Stat(flat=1))

    effect_manager.execute_effect(
        sacred_block_effect,
        monster_4,
        monster_4,
    )

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[Keyword.SACRED_BLOCK],
    )

    conditions = [
        damage_data["damage"] == 0,
        len(damage_data["defended_damage"]) == 2,
        damage_data["defended_damage"]["sacred_block"] == 6,
        damage_data["defended_damage"]["total"] == 6,
    ]

    assert_conditions(conditions)


def test_calculate_damage_invulnerable(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))
    invulnerable_effect = InvulnerableEffect(target_keywords=[Keyword.ALL], duration=1)

    effect_manager.execute_effect(
        invulnerable_effect,
        monster_4,
        monster_4,
    )

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[Keyword.INVULNERABLE],
    )

    conditions = [
        damage_data["damage"] == 0,
        len(damage_data["defended_damage"]) == 2,
        damage_data["defended_damage"]["invulnerable"] == 6,
        damage_data["defended_damage"]["total"] == 6,
    ]

    assert_conditions(conditions)


def test_calculate_damage_multiple(combat: Dict):
    effect_manager: EffectManager = combat["effect_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_4: Monster = combat["monsters"][4]

    attack_effect = AttackEffect(Stat(flat=6))
    block_effect = BlockEffect(Stat(flat=1))
    absorb_effect = AbsorbEffect(Stat(flat=2))

    effect_manager.execute_effect(
        block_effect,
        monster_4,
        monster_4,
    )

    effect_manager.execute_effect(
        absorb_effect,
        monster_4,
        monster_4,
    )

    damage_data = calculate_damage(
        attack_effect,
        monster_0,
        monster_4,
        consider=[Keyword.BLOCK, Keyword.ABSORB],
    )

    conditions = [
        damage_data["damage"] == 3,
        len(damage_data["defended_damage"]) == 3,
        damage_data["defended_damage"]["block"] == 1,
        damage_data["defended_damage"]["absorb"] == 2,
        damage_data["defended_damage"]["total"] == 3,
    ]

    assert_conditions(conditions)
