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
        if not (random() < effect.chance):
            continue

        if effect.keyword == Keyword.ATTACK:
            blinded = source.get_effect(Keyword.BLIND)
            if (blinded) and (random() < effect.value):
                continue

            target.hp -= effect.value

        elif effect.keyword == Keyword.HEAL:
            target.hp += effect.value

        elif effect.keyword == Keyword.BLIND:
            target = overwrite_effect(effect=effect, target=target)

        target.equalize_stats()

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
        current_effect.chance = effect.chance

    else:
        target.effects.append(
            deepcopy(effect)
        )

    return target
