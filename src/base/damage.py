"""Damage module."""

from typing import TypedDict


class DefendedDamage(TypedDict):
    """
    Defended damage data.

    :var absorb: Damage that was defended by a Monster's Absorb effect.
    :vartype absorb: int

    :var block: Damage that was defended by a Monster's Block effect.
    :vartype block: int

    :var invulnerable: Damage that was defended by a Monster's Invulnerable effect.
    :vartype invulnerable: int

    :var sacred_block: Damage that was defended by a Monster's Sacred Block effect.
    :vartype sacred_block: int

    :var total: Total damage that was defended by a Monster's defensive effects.
    :vartype total: int
    """

    absorb: int
    block: int
    invulnerable: int
    sacred_block: int
    total: int


class DamageData(TypedDict):
    """
    Data when calculating damage.

    :var damage: Damage done to a Monster.
    :vartype damage: int

    :var defended_damage: Defended damage data.
    :vartype defended_damage: DefendedDamage
    """

    damage: int
    defended_damage: DefendedDamage
