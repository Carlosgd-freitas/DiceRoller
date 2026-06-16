"""Tests for buff effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.blind import BlindEffect
from src.effects.focus import FocusEffect
from src.effects.heal import HealEffect
from src.effects.immunity import ImmunityEffect
from src.effects.invisible import InvisibleEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.regen import RegenEffect
from src.effects.taunt import TauntEffect
from src.effects.thorns import ThornsEffect
from src.targeting.selectors.offensive_selector import OffensiveSelector
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.manager import CombatManager
    from src.targeting.selectors.manager import SelectorManager


def test_keyword_focus(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_blind = BlindEffect(1, duration=1)
    effect_focus = FocusEffect(1, duration=1)
    effect_heal = HealEffect(2, accuracy=0)
    effect_attack = AttackEffect(2, accuracy=0)

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    combat_manager.effect_manager.execute_effect(
        effect_focus,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.BLIND) is None,
        combat_manager.order[0].get_effect(Keyword.FOCUS).keyword == Keyword.FOCUS,
        combat_manager.order[0].get_effect(Keyword.FOCUS).value == 1,
        combat_manager.order[0].get_effect(Keyword.FOCUS).duration == 1,
        combat_manager.order[0].hp == 1,
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.FOCUS) is None,
        combat_manager.order[1].hp == 10,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            combat_manager.order[0].hp == 3,
            combat_manager.order[1].hp == 8,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            len(combat_manager.order[0].effects) == 0,
            combat_manager.order[0].get_effect(Keyword.FOCUS) is None,
            combat_manager.order[0].hp == 3,
            combat_manager.order[1].hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_keyword_immunity(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_blind = BlindEffect(1, duration=1)
    effect_immunity = ImmunityEffect(effects=[Keyword.BLIND], duration=1)
    effect_attack = AttackEffect(2)

    combat_manager.effect_manager.execute_effect(
        effect_immunity,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.BLIND) is None,
        combat_manager.order[0].get_effect(Keyword.IMMUNITY).keyword
        == Keyword.IMMUNITY,
        combat_manager.order[0].get_effect(Keyword.IMMUNITY).duration == 1,
        combat_manager.order[0].hp == 1,
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.IMMUNITY) is None,
        combat_manager.order[1].hp == 10,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            combat_manager.order[0].hp == 1,
            combat_manager.order[1].hp == 8,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            len(combat_manager.order[0].effects) == 1,
            combat_manager.order[0].get_effect(Keyword.IMMUNITY) is None,
            combat_manager.order[0].get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
            combat_manager.order[0].get_effect(Keyword.BLIND).duration == 1,
            combat_manager.order[0].hp == 1,
            combat_manager.order[1].hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_keyword_invisible(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector_manager: SelectorManager = managers["selector_manager"]

    effect_invisible = InvisibleEffect(duration=1)
    effect_attack = AttackEffect(1)
    effect_heal = HealEffect(1)

    side_attack = Side(effects=[effect_attack])
    side_heal = Side(effects=[effect_heal])

    combat_manager.effect_manager.execute_effect(
        effect_invisible,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.INVISIBLE).keyword
        == Keyword.INVISIBLE,
        combat_manager.order[0].get_effect(Keyword.INVISIBLE).duration == 1,
        combat_manager.order[0].hp == 1,
    ]

    targets: List[Monster] = selector_manager.get_targets(
        side=side_attack,
        source=combat_manager.order[2],
        allies=[combat_manager.order[3]],
        enemies=[combat_manager.order[0], combat_manager.order[1]],
        k=2,
    )

    conditions.extend(
        [
            len(targets) == 1,
            targets[0].local_id == "MONSTER_2",
        ]
    )

    targets: List[Monster] = selector_manager.get_targets(
        side=side_heal,
        source=combat_manager.order[1],
        allies=[combat_manager.order[0]],
        enemies=[combat_manager.order[2], combat_manager.order[3]],
        k=2,
    )

    targets_ids = set([target.local_id for target in targets])

    conditions.extend(
        [
            len(targets) == 2,
            targets_ids == {"MONSTER_1", "MONSTER_2"},
        ]
    )

    combat_manager.end_turn()

    targets: List[Monster] = selector_manager.get_targets(
        side=side_attack,
        source=combat_manager.order[2],
        allies=[combat_manager.order[3]],
        enemies=[combat_manager.order[0], combat_manager.order[1]],
        k=2,
    )

    targets_ids = set([target.local_id for target in targets])

    conditions.extend(
        [
            len(targets) == 2,
            targets_ids == {"MONSTER_1", "MONSTER_2"},
        ]
    )

    assert_conditions(conditions)


def test_keyword_mana_regen(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect = ManaRegenEffect(1, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.MANA_REGEN).keyword
        == Keyword.MANA_REGEN,
        combat_manager.order[1].get_effect(Keyword.MANA_REGEN).value == 1,
        combat_manager.order[1].get_effect(Keyword.MANA_REGEN).duration == 1,
        combat_manager.order[1].mana == 0,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.MANA_REGEN) is None,
            combat_manager.order[1].mana == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_regen(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect = RegenEffect(1, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        combat_manager.order[1].get_effect(Keyword.REGEN).value == 1,
        combat_manager.order[1].get_effect(Keyword.REGEN).duration == 1,
        combat_manager.order[1].hp == 10,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.REGEN) is None,
            combat_manager.order[1].hp == 11,
        ]
    )

    assert_conditions(conditions)


def test_keyword_taunt(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector = OffensiveSelector()

    combat_manager.current_monster = combat_manager.order[1]

    effect_taunt = TauntEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_taunt,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.TAUNT).keyword == Keyword.TAUNT,
        combat_manager.order[1].get_effect(Keyword.TAUNT).duration == 1,
        combat_manager.order[1].hp == 10,
    ]

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            combat_manager.order[0],
            combat_manager.order[1],
            combat_manager.order[2],
        ],
        k=1,
    )

    conditions.extend(
        [
            len(targets) == 1,
            targets[0].local_id == "MONSTER_2",
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.TAUNT) is None,
        ]
    )

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            combat_manager.order[0],
            combat_manager.order[1],
            combat_manager.order[2],
        ],
        k=1,
    )

    conditions.extend(
        [
            len(targets) == 1,
            targets[0].local_id == "MONSTER_1",
        ]
    )

    assert_conditions(conditions)


def test_keyword_thorns(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    attack_effect = AttackEffect(4)
    thorns_effect = ThornsEffect(4, duration=1)

    combat_manager.effect_manager.execute_effect(
        thorns_effect,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        combat_manager.order[1].hp == 10,
        combat_manager.order[1].get_effect(Keyword.THORNS).keyword == Keyword.THORNS,
        combat_manager.order[1].get_effect(Keyword.THORNS).value == 4,
        combat_manager.order[2].local_id == "MONSTER_3",
        combat_manager.order[2].get_effect(Keyword.THORNS) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=combat_manager.order[2],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            combat_manager.order[1].hp == 6,
            combat_manager.order[1].get_effect(Keyword.THORNS).keyword
            == Keyword.THORNS,
            combat_manager.order[1].get_effect(Keyword.THORNS).value == 4,
            combat_manager.order[2].hp == 96,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=combat_manager.order[2],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            combat_manager.order[1].hp == 2,
            combat_manager.order[1].get_effect(Keyword.THORNS) is None,
            combat_manager.order[2].hp == 96,
        ]
    )

    assert_conditions(conditions)
