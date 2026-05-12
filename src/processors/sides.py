"""Sides processor module."""

from typing import List
from src.base.side import Side
from src.base.monster import Monster


def process_side(
    side: Side,
    source: Monster,
    targets: List[Monster]
) -> List[Monster]:
    for target in targets:
        for effect in side.effects:
            effect.activate(
                source,
                target,
            )

    return targets
