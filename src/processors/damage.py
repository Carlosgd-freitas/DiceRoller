"""Damage processor module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List, TypedDict

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Entity


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


def calculate_damage(
    effect: Effect,
    source: Entity,
    target: Entity,
    consider: List[Keyword] = None,
) -> DamageData:
    """
    Calculate damage which will be done to a target.

    :param effect: The effect used to calculate the damage.
    :type effect: Effect

    :param source: The Entity object where the effect is from.
    :type source: Entity

    :param target: An Entity object which the effect will be applied.
    :type target: Entity

    :param consider: A list of defensive effect keywords to be considered on damage
    calculation. By default, only the Invulnerable effect is considered.
    :type consider: List[Keyword]

    The priority of defensive effect activation is:
    * Invulnerable
    * Sacred Block
    * Absorb
    * Block

    :return: The damage caused on the target Entity.
    :rtype: int
    """
    consider = [Keyword.INVULNERABLE] if consider is None else consider
    damage = effect.get_effective_value(source, target)
    defended_damage: DefendedDamage = {}

    # Invulnerable
    if Keyword.INVULNERABLE in consider:
        invulnerable = target.get_effect(Keyword.INVULNERABLE)

        if invulnerable:
            defended_damage["invulnerable"] = damage
            damage = 0

    # Sacred Block
    if Keyword.SACRED_BLOCK in consider:
        sacred_blocking = target.get_effect(Keyword.SACRED_BLOCK)

        if (damage > 0) and (sacred_blocking):
            defended_damage["sacred_block"] = damage
            damage = 0

            sacred_blocking.value -= 1

            if sacred_blocking.value <= 0:
                target.effects.remove(sacred_blocking)

    # Absorb
    if Keyword.ABSORB in consider:
        absorbing = target.get_effect(Keyword.ABSORB)

        if (damage > 0) and (absorbing):
            absorbed_damage = min(damage, absorbing.value)
            defended_damage["absorb"] = absorbed_damage

            damage -= absorbed_damage
            absorbing.value -= absorbed_damage

            target.hp += absorbed_damage
            target.equalize_stats()

            if absorbing.value <= 0:
                target.effects.remove(absorbing)

    # Block
    if Keyword.BLOCK in consider:
        blocking = target.get_effect(Keyword.BLOCK)

        if (damage > 0) and (blocking):
            blocked_damage = min(damage, blocking.value)
            defended_damage["block"] = blocked_damage

            damage -= blocked_damage
            blocking.value -= blocked_damage

            if blocking.value <= 0:
                target.effects.remove(blocking)

    if damage < 0:
        damage = 0

    # Total defended damage
    total_defended_damage = 0

    for value in defended_damage.values():
        total_defended_damage += value

    if total_defended_damage:
        defended_damage["total"] = total_defended_damage

    return {
        "damage": damage,
        "defended_damage": defended_damage,
    }
