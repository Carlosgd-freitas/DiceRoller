"""Damage processor module."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.damage import DamageData, DefendedDamage
    from src.base.effect import Effect
    from src.base.monster import Entity


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

            sacred_blocking.value.flat -= 1

            if sacred_blocking.value.flat <= 0:
                target.effects.remove(sacred_blocking)

    # Absorb
    if Keyword.ABSORB in consider:
        absorbing = target.get_effect(Keyword.ABSORB)

        if (damage > 0) and (absorbing):
            absorbed_damage = min(damage, absorbing.value.flat)
            defended_damage["absorb"] = absorbed_damage

            damage -= absorbed_damage
            absorbing.value.flat -= absorbed_damage

            target.hp += absorbed_damage
            target.equalize_stats()

            if absorbing.value.flat <= 0:
                target.effects.remove(absorbing)

    # Block
    if Keyword.BLOCK in consider:
        blocking = target.get_effect(Keyword.BLOCK)

        if (damage > 0) and (blocking):
            blocked_damage = min(damage, blocking.value.flat)
            defended_damage["block"] = blocked_damage

            damage -= blocked_damage
            blocking.value.flat -= blocked_damage

            if blocking.value.flat <= 0:
                target.effects.remove(blocking)

    if damage < 0:
        damage = 0
    elif target.hp - damage < 0:
        damage = target.hp

    # Total defended damage
    total = 0

    for value in defended_damage.values():
        total += value

    if total:
        defended_damage["total"] = total

    return {
        "damage": damage,
        "defended_damage": defended_damage,
    }
