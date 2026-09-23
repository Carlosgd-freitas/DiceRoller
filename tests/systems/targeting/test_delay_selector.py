"""Tests for DelaySelector class."""

from typing import Dict, List

from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.stat import Stat
from src.effects.burn import BurnEffect
from src.effects.delay import DelayEffect
from src.effects.regen import RegenEffect
from src.systems.targeting.selectors.delay_selector import DelaySelector
from tests.utils import assert_conditions


def test_delay_selector_targeting(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = DelaySelector()

    effect_regen = RegenEffect(Stat(flat=1), duration=1)
    monsters[2].effects = [effect_regen]

    effect_delay = DelayEffect(Stat(flat=1), target_keywords=[Keyword.REGEN])

    filtered = selector.get_targets_hard(
        source=monsters[1],
        allies=[monsters[2], monsters[4]],
        enemies=[monsters[3]],
        k=1,
        main_effect=effect_delay,
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_2",
    ]

    effect_burn = BurnEffect(Stat(flat=1), duration=1)
    monsters[4].effects = [effect_burn]

    effect_delay = DelayEffect(Stat(flat=1), target_keywords=[Keyword.BURN])

    filtered = selector.get_targets_hard(
        source=monsters[1],
        allies=[monsters[2]],
        enemies=[monsters[3], monsters[4]],
        k=1,
        main_effect=effect_delay,
    )

    conditions.extend(
        [
            len(filtered) == 1,
            filtered[0].local_id == "MONSTER_4",
        ]
    )

    assert_conditions(conditions)
