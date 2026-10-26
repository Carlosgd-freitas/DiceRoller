"""Tests for Area class."""

from src.areas.grasslands import Grasslands
from src.monsters.slime import Slime
from src.nodes.battle_node import BattleNode
from src.nodes.boss_battle_node import BossBattleNode
from tests.utils import assert_conditions


def test_area_get_encounter():
    area = Grasslands()

    encounter_entries = area.get_enemies()

    encounter = area.get_encounter(
        encounter_entries,
        k=1,
    )
    conditions = [
        len(encounter.members) == 1,
    ]

    encounter = area.get_encounter(
        encounter_entries,
        k=None,
        path_level=3,
        ratio=2,
    )
    conditions.extend(
        [
            len(encounter.members) == 2,
        ]
    )

    assert_conditions(conditions)


def test_area_get_encounter_repeat_monster():
    area = Grasslands()

    encounter_entries = [
        {
            "monster_global_id": "SLIME",
            "weight": 1,
            "role": "DAMAGE",
        }
    ]

    encounter = area.get_encounter(
        encounter_entries,
        k=2,
    )

    conditions = [
        len(encounter.members) == 2,
        all([isinstance(monster, Slime) for monster in encounter.members]),
    ]

    assert_conditions(conditions)


def test_area_setup_node():
    area = Grasslands()

    battle_node = BattleNode()
    area.setup_node(battle_node)
    conditions = [
        len(battle_node.encounter.members) > 0,
    ]

    boss_battle_node = BossBattleNode()
    area.setup_node(boss_battle_node)
    conditions.extend(
        [
            len(boss_battle_node.encounter.members) > 0,
        ]
    )

    assert_conditions(conditions)
