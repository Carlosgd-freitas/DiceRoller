"""Damage processor module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Entity


def calculate_damage(
    effect: Effect,
    source: Entity,
    target: Entity,
    consider_block: bool = False,
) -> int:
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

    if consider_block:
        # Absorb
        absorbing = target.get_effect(Keyword.ABSORB)

        if absorbing:
            min_value = min(damage, absorbing.value)

            damage -= min_value
            absorbing.value -= min_value

            target.hp += min_value
            target.equalize_stats()

            if absorbing.value <= 0:
                target.effects.remove(absorbing)

        # Block
        blocking = target.get_effect(Keyword.BLOCK)

        if blocking:
            min_value = min(damage, blocking.value)

            damage -= min_value
            blocking.value -= min_value

            if blocking.value <= 0:
                target.effects.remove(blocking)

    if damage < 0:
        damage = 0

    return damage
