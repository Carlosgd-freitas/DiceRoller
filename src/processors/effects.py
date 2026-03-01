"""Effects processor module."""

from random import random
from copy import deepcopy
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword
from typing import Literal, List, Tuple

type stack_method = Literal["add", "overwrite"]
type effect_param = Literal["value", "duration", "decay", "accuracy", "dispellable"]


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
        stunned = source.get_effect(Keyword.STUN)
        if (stunned):
            continue

        # Blind check
        blinded = source.get_effect(Keyword.BLIND)
        if (blinded) and (target.local_id != source.local_id):
            accuracy -= blinded.value

        # Accuracy check
        if not (chance < accuracy):
            continue

        if effect.keyword in [Keyword.ATTACK, Keyword.CURSE]:
            target.hp -= effect.value

        elif effect.keyword in [Keyword.BLIND, Keyword.STUN]:
            target = stack_effect(
                effect=effect,
                target=target,
                rules=[
                    ("add", "value"),
                    ("add", "duration"),
                ],
            )

        elif effect.keyword == Keyword.HEAL:
            target.hp += effect.value

        elif effect.keyword == Keyword.MANA:
            target.mana += effect.value

        target.equalize_stats()
    
    source.equalize_stats()

    return targets


def stack_effect(
    effect: Effect,
    target: Monster,
    rules: List[Tuple[stack_method, effect_param]] = None,
    remove: List[Keyword] = None,
) -> Monster:
    """
    Stack a effect in a targeted monster.

    :param effect: The effect that will be stacked.
    :type effect: Effect

    :param target: The Monster object where the effect will be stacked.
    :type target: Monster

    :param rules: A list of (X, Y) tuples describing how the effect is stacked, where X
    is the stack method itself and Y is the Effect parameter name.
    :type rules: List[Tuple[stack_method, effect_param]]

    :param remove: A list of Keywords. Any effects on the target that has one of these
    keywords will be removed.
    :type remove: List[Keyword]

    :return: A Monster object after the effect has been stacked.
    :rtype: Monster

    **Stack Methods*
    * ``add``: if the monster has an existing effect with the same Keyword, the values
    of the existing effect and the new effect for that parameter will be added

    * ``overwrite``: if the monster has an existing effect with the same Keyword, the
    value of the existing effect will be overwritten by the new effect for that
    parameter

    **Effect Parameters**
    * value
    * duration
    * decay
    * accuracy
    * dispellable
    """
    remove = [] if remove is None else list(remove)
    rules = [] if rules is None else list(rules)

    # Remove effects
    for keyword in remove:
        effect_to_remove = target.get_effect(keyword)
        if effect_to_remove:
            target.effects.remove(effect_to_remove)

    # Stack effect
    current_effect = target.get_effect(effect.keyword)

    if current_effect:
        for method, param in rules:
            current_effect_value = getattr(current_effect, param) or 0
            new_effect_value = getattr(effect, param) or 0

            if method == "add":
                setattr(
                    current_effect,
                    param,
                    current_effect_value+new_effect_value,
                )

            elif method == "overwrite":
                setattr(
                    current_effect,
                    param,
                    new_effect_value,
                )

    else:
        target.effects.append(
            deepcopy(effect)
        )

    return target
