"""Healing processor module."""

from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.base.effect import Effect
    from src.base.monster import Entity


def calculate_healing(
    effect: Effect,
    source: Entity,
    target: Entity,
) -> int:
    """
    Calculate healing which will be done to a target.

    :param effect: The effect used to calculate the heal.
    :type effect: Effect

    :param source: The Entity object where the effect is from.
    :type source: Entity

    :param target: An Entity object which the effect will be applied.
    :type target: Entity

    :return: The healed amount on the target Entity.
    :rtype: int
    """
    healed = effect.get_effective_value(source, target)

    healed += ceil(target.max_hp * effect.get_effective_value_percent(source, target))

    if healed < 0:
        healed = 0
    if target.hp + healed > target.max_hp:
        healed = target.max_hp - target.hp

    return healed
