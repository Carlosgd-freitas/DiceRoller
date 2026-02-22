"""Effects processor module."""

from typing import List
from random import random
from copy import deepcopy
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword


def process_effect(
    effect: Effect,
    source: Monster,
    targets: List[Monster]
) -> List[Monster]:
    for target in targets:
        accuracy = effect.accuracy

        # Blind check
        blinded = source.get_effect(Keyword.BLIND)
        if (blinded) and (target.local_id != source.local_id):
            accuracy -= blinded.value

        # Accuracy check
        if not (random() < accuracy):
            continue

        if effect.keyword in [Keyword.ATTACK, Keyword.CURSE]:
            target.hp -= effect.value

        elif effect.keyword == Keyword.BLIND:
            target = overwrite_effect(effect=effect, target=target)

        elif effect.keyword == Keyword.HEAL:
            target.hp += effect.value

        elif effect.keyword == Keyword.MANA:
            target.mana += effect.value

        target.equalize_stats()
    
    source.equalize_stats()

    return targets


def overwrite_effect(
    effect: Effect,
    target: Monster
) -> Monster:
    current_effect = target.get_effect(effect.keyword)

    if current_effect:
        current_effect.value = effect.value
        current_effect.duration = effect.duration
        current_effect.decay = effect.decay
        current_effect.accuracy = effect.accuracy

    else:
        target.effects.append(
            deepcopy(effect)
        )

    return target
