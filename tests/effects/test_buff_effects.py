"""Tests for buff effects processing."""

from typing import Dict

from src.base.keywords import Keyword
from src.combat.manager import CombatManager
from src.effects.attack import AttackEffect
from src.effects.thorns import ThornsEffect
from tests.utils import assert_conditions


def test_keyword_thorns(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[2]

    attack_effect = AttackEffect(4)
    thorns_effect = ThornsEffect(4, duration=1)

    combat_manager.order[2].apply_effect(thorns_effect)

    conditions = [
        combat_manager.order[2].local_id == "MONSTER_2",
        combat_manager.order[2].hp == 10,
        combat_manager.order[2].get_effect(Keyword.THORNS).keyword == Keyword.THORNS,
        combat_manager.order[2].get_effect(Keyword.THORNS).value == 4,
        combat_manager.order[3].local_id == "MONSTER_3",
        combat_manager.order[3].get_effect(Keyword.THORNS) is None,
    ]

    combat_manager.activate_effect(
        attack_effect,
        source=combat_manager.order[3],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            combat_manager.order[2].hp == 6,
            combat_manager.order[2].get_effect(Keyword.THORNS).keyword
            == Keyword.THORNS,
            combat_manager.order[2].get_effect(Keyword.THORNS).value == 4,
            combat_manager.order[3].hp == 96,
        ]
    )

    combat_manager.end_turn()

    combat_manager.activate_effect(
        attack_effect,
        source=combat_manager.order[3],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            combat_manager.order[2].hp == 2,
            combat_manager.order[2].get_effect(Keyword.THORNS) is None,
            combat_manager.order[3].hp == 96,
        ]
    )

    assert_conditions(conditions)
