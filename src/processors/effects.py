"""Effects processor module."""

from typing import List
from random import random
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword


def apply_damage(
    effect: Effect,
    source: Monster,
    target: Monster,
    consider_block: bool = True,
) -> int:
    """
    Calculate and apply damage directly to a target.

    :param effect: The damaging effect that will be processed.
    :type effect: Effect

    :param source: The Monster object where the damaging Effect is from.
    :type source: Monster

    :param target: A Monster object which the damaging effect will be applied.
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


def process_effect(
    effect: Effect,
    source: Monster,
    targets: List[Monster]
) -> List[Monster]:
    """
    Process a effect in a list of targeted monsters.

    :param effect: The effect that will be processed.
    :type effect: Effect

    :param source: The Monster object where the Effect is from.
    :type source: Monster

    :param targets: A list of Monster objects which the effect will be applied.
    :type targets: List[Monster]

    :return: A list of Monster objects after the effect has been processed.
    :rtype: List[Monster]
    """
    for target in targets:
        chance = random()
        accuracy = effect.accuracy

        # Stun check
        # stunned = source.get_effect(Keyword.STUN)
        # if (stunned):
        #     continue

        # Blind check
        # blinded = source.get_effect(Keyword.BLIND)
        # if (blinded) and (target.local_id != source.local_id):
        #     accuracy -= blinded.value

        # Accuracy check
        if not (chance < accuracy):
            continue

        # Damage
        if effect.keyword == Keyword.ATTACK:
            damage = apply_damage(
                effect=effect,
                source=source,
                target=target,
                consider_block=True,
            )

        elif effect.keyword in [
            Keyword.BLEED,
            Keyword.BURN,
            Keyword.CURSE,
            Keyword.PIERCE,
            Keyword.POISON,
        ]:
            damage = apply_damage(
                effect=effect,
                source=source,
                target=target,
                consider_block=False,
            )
        
        elif effect.keyword == Keyword.DRAIN:
            damage = apply_damage(
                effect=effect,
                source=source,
                target=target,
                consider_block=True,
            )
            source.hp += damage

        # Heal
        elif effect.keyword in [Keyword.HEAL, Keyword.REGEN]:
            target.hp += effect.value

        # Mana
        elif effect.keyword in [Keyword.MANA, Keyword.MANA_REGEN]:
            target.mana += effect.value

        if target:
            target.equalize_stats()

        if (source) and (target != source):
            source.equalize_stats()

    return targets
