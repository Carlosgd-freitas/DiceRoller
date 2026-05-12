"""Damage processor module."""

from __future__ import annotations

from typing import TYPE_CHECKING
from src.base.keywords import Keyword

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Entity
    

def calculate_damage(
    effect: Effect,
    source: "Entity",
    target: "Entity",
    consider_block: bool = False,
) -> int:
    """
    Calculate damage which will be done to a target.

    :param effect: The effect used to calculate the damage.
    :type effect: Effect

    :param source: The Entity object where the effect is from.
    :type source: Entity

    :param target: A Entity object which the effect will be applied.
    :type target: Entity

    :param consider_block: If Block effect on the target will reduce the damage.
    :type consider_block: bool

    :return: The damage caused on the target Entity.
    :rtype: int
    """
    damage = effect.value

    if consider_block:
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
