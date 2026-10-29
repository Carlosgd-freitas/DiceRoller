"""Tests for HurrySelector class."""

from typing import Dict, List

from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.stat import Stat
from src.effects.burn import BurnEffect
from src.effects.hurry import HurryEffect
from src.effects.regen import RegenEffect
from src.systems.targeting.selectors.hurry_selector import HurrySelector
from tests.utils import assert_conditions


def test_hurry_selector_targeting(combat: Dict):
    monsters: List[Monster] = combat["monsters"]
    selector = HurrySelector()

    effect_regen = RegenEffect(Stat(flat=1), duration=1)
    monsters[2].effects = [effect_regen]

    effect_hurry = HurryEffect(Stat(flat=1), target_keywords=[Keyword.REGEN])

    filtered = selector.get_targets_hard(
        source=monsters[1],
        allies=[monsters[4]],
        enemies=[monsters[2], monsters[3]],
        k=1,
        main_effect=effect_hurry,
    )

    conditions = [
        len(filtered) == 1,
        filtered[0].local_id == "MONSTER_2",
    ]

    effect_burn = BurnEffect(Stat(flat=1), duration=1)
    monsters[4].effects = [effect_burn]

    effect_hurry = HurryEffect(Stat(flat=1), target_keywords=[Keyword.BURN])

    filtered = selector.get_targets_hard(
        source=monsters[1],
        allies=[monsters[3], monsters[4]],
        enemies=[monsters[2]],
        k=1,
        main_effect=effect_hurry,
    )

    conditions.extend(
        [
            len(filtered) == 1,
            filtered[0].local_id == "MONSTER_4",
        ]
    )

    assert_conditions(conditions)
