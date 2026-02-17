"""Sides processor module."""

from typing import List
from src.base.side import Side
from src.base.monster import Monster
from src.processors.effects import process_effect


def process_side(
    side: Side,
    source: Monster,
    targets: List[Monster]
) -> List[Monster]:
    for effect in side.effects:
        targets = process_effect(
            effect=effect,
            source=source,
            targets=targets,
        )

    return targets
