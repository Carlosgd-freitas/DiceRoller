"""Damage processor module."""

from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword


def calculate_damage(
    effect: Effect,
    source: Monster,
    target: Monster,
    consider_block: bool = True,
) -> int:
    """
    Calculate damage which will be done to a target.

    :param effect: The effect that will be processed.
    :type effect: Effect

    :param source: The Monster object where the Effect is from.
    :type source: Monster

    :param target: A Monster object which the effect will be applied.
    :type target: Monster

    :return: The damage caused on the target Monster.
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

    target.hp -= damage

    return damage
