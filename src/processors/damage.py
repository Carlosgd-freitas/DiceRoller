"""Damage processor module."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Entity


class DamageData(TypedDict):
    """
    Data when calculating damage.

    :var absorbed_damage: Damage that was absorbed by a Monster.
    :vartype absorbed_damage: int

    :var blocked_damage: Damage that was blocked by a Monster.
    :vartype blocked_damage: int

    :var damage: Damage done to a Monster.
    :vartype damage: int

    :var total_blocked_damage: Total damage that was blocked by a Monster's defensive
    Effects.
    :vartype total_blocked_damage: int
    """

    absorbed_damage: int
    blocked_damage: int
    damage: int
    total_blocked_damage: int


def calculate_damage(
    effect: Effect,
    source: Entity,
    target: Entity,
    consider_block: bool = False,
) -> DamageData:
    """
    Calculate damage which will be done to a target.

    :param effect: The effect used to calculate the damage.
    :type effect: Effect

    :param source: The Entity object where the effect is from.
    :type source: Entity

    :param target: An Entity object which the effect will be applied.
    :type target: Entity

    :param consider_block: If Block or Absorb effects on the target will reduce the
    damage. Absorb has priority over Block.
    :type consider_block: bool

    :return: The damage caused on the target Entity.
    :rtype: int
    """
    damage = effect.value
    absorbed_damage = 0
    blocked_damage = 0

    if consider_block:
        # Absorb
        absorbing = target.get_effect(Keyword.ABSORB)

        if (damage > 0) and (absorbing):
            absorbed_damage = min(damage, absorbing.value)

            damage -= absorbed_damage
            absorbing.value -= absorbed_damage

            target.hp += absorbed_damage
            target.equalize_stats()

            if absorbing.value <= 0:
                target.effects.remove(absorbing)

        # Block
        blocking = target.get_effect(Keyword.BLOCK)

        if (damage > 0) and (blocking):
            blocked_damage = min(damage, blocking.value)

            damage -= blocked_damage
            blocking.value -= blocked_damage

            if blocking.value <= 0:
                target.effects.remove(blocking)

    if damage < 0:
        damage = 0

    total_blocked_damage = absorbed_damage + blocked_damage

    return {
        "absorbed_damage": absorbed_damage,
        "blocked_damage": blocked_damage,
        "damage": damage,
        "total_blocked_damage": total_blocked_damage,
    }
