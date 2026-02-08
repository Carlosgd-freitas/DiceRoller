"""Effects processor module."""

from typing import List
from src.base.effect import Effect
from src.base.monster import Monster
from src.base.keywords import Keyword


def process_effect(
    effect: Effect,
    targets: List[Monster]
) -> List[Monster]:
    for target in targets:
        if effect.keyword == Keyword.ATTACK:
            target.hp -= effect.value
        
        elif effect.keyword == Keyword.HEAL:
            target.hp += effect.value
        
        target.equalize_stats()

    return targets
