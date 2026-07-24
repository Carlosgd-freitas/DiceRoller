"""Tests for buff effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.keywords import Keyword
from src.base.side import Side
from src.base.stat import Stat
from src.combat.manager import CombatManager, OrderStrategy
from src.effects.attack import AttackEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.focus import FocusEffect
from src.effects.fortify import FortifyEffect
from src.effects.haste import HasteEffect
from src.effects.heal import HealEffect
from src.effects.immunity import ImmunityEffect
from src.effects.invisible import InvisibleEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.regen import RegenEffect
from src.effects.repel import RepelEffect
from src.effects.slow import SlowEffect
from src.effects.strength import StrengthEffect
from src.effects.taunt import TauntEffect
from src.effects.thorns import ThornsEffect
from src.systems.targeting.selectors.offensive_selector import OffensiveSelector
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.systems.targeting.selectors.manager import SelectorManager


def test_focus_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect_blind = BlindEffect(Stat(percent=1), duration=1)
    effect_focus = FocusEffect(Stat(percent=1), duration=1)
    effect_heal = HealEffect(Stat(flat=2), accuracy=0)
    effect_attack = AttackEffect(Stat(flat=2), accuracy=0)

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        effect_focus,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.BLIND) is None,
        monster_1.get_effect(Keyword.FOCUS).keyword == Keyword.FOCUS,
        monster_1.get_effect(Keyword.FOCUS).value == Stat(flat=None, percent=1),
        monster_1.get_effect(Keyword.FOCUS).duration == 1,
        monster_1.hp == 1,
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 0,
        monster_2.get_effect(Keyword.FOCUS) is None,
        monster_2.hp == 10,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_1.hp == 3,
            monster_2.hp == 8,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_1.effects) == 0,
            monster_1.get_effect(Keyword.FOCUS) is None,
            monster_1.hp == 3,
            monster_2.hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_fortify_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]

    block_effect = BlockEffect(Stat(flat=3), duration=1)
    fortify_effect = FortifyEffect(Stat(flat=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        fortify_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.FORTIFY).keyword == Keyword.FORTIFY,
        monster_1.get_effect(Keyword.FORTIFY).value == Stat(flat=2, percent=None),
        monster_1.get_effect(Keyword.FORTIFY).duration == 1,
    ]

    combat_manager.effect_manager.execute_effect(
        block_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions.extend(
        [
            len(monster_1.effects) == 2,
            monster_1.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=5, percent=None),
            monster_1.get_effect(Keyword.BLOCK).duration == 1,
        ]
    )

    combat_manager.end_turn()

    monster_1.effects = []

    fortify_effect = FortifyEffect(Stat(percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        fortify_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        block_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions.extend(
        [
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=6, percent=None),
        ]
    )

    combat_manager.end_turn()

    monster_1.effects = []

    fortify_effect = FortifyEffect(Stat(flat=1, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        fortify_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        block_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions.extend(
        [
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=8, percent=None),
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        block_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions.extend(
        [
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=3, percent=None),
        ]
    )

    assert_conditions(conditions)


def test_haste_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.order_strategy = OrderStrategy.FASTER
    combat_manager.start_combat()

    turn_local_ids = []

    combat_manager.start_round()
    for turn in range(4):
        turn_local_ids.append(combat_manager.current_monster.local_id)

        if turn == 0:
            haste_effect = HasteEffect(Stat(flat=100), duration=1)

            combat_manager.effect_manager.execute_effect(
                haste_effect,
                source=combat_manager.current_monster,
                target=monster_2,
            )

            conditions = [
                monster_2.local_id == "MONSTER_2",
                len(monster_2.effects) == 1,
                monster_2.get_effect(Keyword.HASTE).keyword == Keyword.HASTE,
                monster_2.get_effect(Keyword.HASTE).value == Stat(flat=100),
                monster_2.get_effect(Keyword.HASTE).duration == 1,
                monster_2.speed == 1,
                monster_2.get_effective_speed() == 101,
            ]

        combat_manager.current_monster.turn_taken = True
        combat_manager.end_turn()
        combat_manager.next_turn()
    combat_manager.end_round()

    conditions.extend(
        [
            turn_local_ids[0] == "MONSTER_3",
            turn_local_ids[1] == "MONSTER_2",
            turn_local_ids[2] == "MONSTER_1",
            turn_local_ids[3] == "MONSTER_4",
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.HASTE) is None,
            monster_2.speed == 1,
            monster_2.get_effective_speed() == 1,
        ]
    )

    turn_local_ids = []

    combat_manager.start_round()
    for _ in range(4):
        turn_local_ids.append(combat_manager.current_monster.local_id)
        combat_manager.current_monster.turn_taken = True
        combat_manager.end_turn()
        combat_manager.next_turn()
    combat_manager.end_round()

    conditions.extend(
        [
            turn_local_ids[0] == "MONSTER_3",
            turn_local_ids[1] == "MONSTER_1",
            turn_local_ids[2] == "MONSTER_2",
            turn_local_ids[3] == "MONSTER_4",
        ]
    )

    slow_effect = SlowEffect(Stat(flat=100), duration=1)
    haste_effect = HasteEffect(Stat(percent=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        slow_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        haste_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == 3,
        ]
    )

    monster_2.effects = []

    haste_effect = HasteEffect(Stat(flat=1, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        haste_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == 3,
        ]
    )

    assert_conditions(conditions)


def test_immunity_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect_blind = BlindEffect(Stat(percent=1), duration=1)
    effect_immunity = ImmunityEffect(target_keywords=[Keyword.BLIND], duration=1)
    effect_attack = AttackEffect(Stat(flat=2))

    combat_manager.effect_manager.execute_effect(
        effect_immunity,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.BLIND) is None,
        monster_1.get_effect(Keyword.IMMUNITY).keyword == Keyword.IMMUNITY,
        monster_1.get_effect(Keyword.IMMUNITY).duration == 1,
        monster_1.hp == 1,
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 0,
        monster_2.get_effect(Keyword.IMMUNITY) is None,
        monster_2.hp == 10,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_1.hp == 1,
            monster_2.hp == 8,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        effect_blind,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_1,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_1.effects) == 1,
            monster_1.get_effect(Keyword.IMMUNITY) is None,
            monster_1.get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
            monster_1.get_effect(Keyword.BLIND).duration == 1,
            monster_1.hp == 1,
            monster_2.hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_invisible_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    selector_manager: SelectorManager = combat["selector_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]
    monster_4: Monster = combat["monsters"][4]

    effect_invisible = InvisibleEffect(duration=1)
    effect_attack = AttackEffect(Stat(flat=1))
    effect_heal = HealEffect(Stat(flat=1))

    side_attack = Side(effects=[effect_attack])
    side_heal = Side(effects=[effect_heal])

    combat_manager.effect_manager.execute_effect(
        effect_invisible,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.INVISIBLE).keyword == Keyword.INVISIBLE,
        monster_1.get_effect(Keyword.INVISIBLE).duration == 1,
        monster_1.hp == 1,
    ]

    targets: List[Monster] = selector_manager.get_targets(
        side=side_attack,
        source=monster_3,
        allies=[monster_4],
        enemies=[monster_1, monster_2],
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
        source=monster_2,
        allies=[monster_1],
        enemies=[monster_3, monster_4],
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
        source=monster_3,
        allies=[monster_4],
        enemies=[monster_1, monster_2],
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


def test_mana_regen_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster: Monster = combat["monsters"][2]

    combat_manager.current_monster = monster

    effect = ManaRegenEffect(Stat(flat=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions = [
        monster.local_id == "MONSTER_2",
        len(monster.effects) == 1,
        monster.get_effect(Keyword.MANA_REGEN).keyword == Keyword.MANA_REGEN,
        monster.get_effect(Keyword.MANA_REGEN).value == Stat(flat=1, percent=None),
        monster.get_effect(Keyword.MANA_REGEN).duration == 1,
        monster.mana == 0,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster.effects) == 0,
            monster.get_effect(Keyword.MANA_REGEN) is None,
            monster.mana == 1,
        ]
    )

    effect = ManaRegenEffect(Stat(percent=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.get_effect(Keyword.MANA_REGEN).value == Stat(flat=None, percent=2),
        ]
    )

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            monster.mana == 3,
        ]
    )

    effect = ManaRegenEffect(Stat(flat=1, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.get_effect(Keyword.MANA_REGEN).value == Stat(flat=1, percent=1),
        ]
    )

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            monster.mana == 7,
        ]
    )

    assert_conditions(conditions)


def test_regen_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster: Monster = combat["monsters"][2]

    combat_manager.current_monster = monster

    effect = RegenEffect(Stat(flat=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions = [
        monster.local_id == "MONSTER_2",
        len(monster.effects) == 1,
        monster.get_effect(Keyword.REGEN).keyword == Keyword.REGEN,
        monster.get_effect(Keyword.REGEN).value == Stat(flat=1, percent=None),
        monster.get_effect(Keyword.REGEN).duration == 1,
        monster.hp == 10,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster.effects) == 0,
            monster.get_effect(Keyword.REGEN) is None,
            monster.hp == 11,
        ]
    )

    effect = RegenEffect(Stat(percent=0.1), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.get_effect(Keyword.REGEN).value == Stat(flat=None, percent=0.1),
        ]
    )

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            monster.hp == 26,
        ]
    )

    effect = RegenEffect(Stat(flat=1, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster,
        target=monster,
    )

    conditions.extend(
        [
            monster.get_effect(Keyword.REGEN).value == Stat(flat=1, percent=1),
        ]
    )

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            monster.hp == monster.max_hp,
        ]
    )

    assert_conditions(conditions)


def test_repel_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    selector = OffensiveSelector()
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]

    combat_manager.current_monster = monster_2

    effect_repel = RepelEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_repel,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.REPEL).keyword == Keyword.REPEL,
        monster_2.get_effect(Keyword.REPEL).duration == 1,
        monster_2.hp == 10,
    ]

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            monster_1,
            monster_2,
            monster_3,
        ],
        k=2,
    )

    targets_ids = set([target.local_id for target in targets])

    conditions.extend(
        [
            len(targets) == 2,
            targets_ids == {"MONSTER_1", "MONSTER_3"},
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.REPEL) is None,
        ]
    )

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            monster_1,
            monster_2,
            monster_3,
        ],
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


def test_taunt_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    selector = OffensiveSelector()
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]

    combat_manager.current_monster = monster_2

    effect_taunt = TauntEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_taunt,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.TAUNT).keyword == Keyword.TAUNT,
        monster_2.get_effect(Keyword.TAUNT).duration == 1,
        monster_2.hp == 10,
    ]

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            monster_1,
            monster_2,
            monster_3,
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
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.TAUNT) is None,
        ]
    )

    targets: List[Monster] = selector._get_targets_lowest_hp(
        monsters=[
            monster_1,
            monster_2,
            monster_3,
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


def test_strength_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_3: Monster = combat["monsters"][3]

    attack_effect = AttackEffect(Stat(flat=2))
    strength_effect = StrengthEffect(Stat(flat=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        strength_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        monster_1.hp == 1,
        len(monster_1.effects) == 1,
        monster_3.local_id == "MONSTER_3",
        monster_3.get_effect(Keyword.STRENGTH) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_1,
        target=monster_3,
    )

    conditions.extend(
        [
            len(monster_1.effects) == 1,
            monster_1.get_effect(Keyword.STRENGTH).keyword == Keyword.STRENGTH,
            monster_1.get_effect(Keyword.STRENGTH).value == Stat(flat=1, percent=None),
            monster_1.get_effect(Keyword.STRENGTH).duration == 1,
            monster_3.hp == 97,
        ]
    )

    combat_manager.end_turn()

    strength_effect = StrengthEffect(Stat(percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        strength_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_1,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_3.hp == 93,
        ]
    )

    combat_manager.end_turn()

    strength_effect = StrengthEffect(Stat(flat=1, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        strength_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_1,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_3.hp == 87,
        ]
    )

    combat_manager.end_turn()

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_1,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_1.hp == 1,
            len(monster_1.effects) == 0,
            monster_1.get_effect(Keyword.STRENGTH) is None,
            monster_3.hp == 85,
        ]
    )

    combat_manager.end_turn()

    assert_conditions(conditions)


def test_thorns_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    monster_0.hp = 100
    monster_1.hp = 100

    attack_effect = AttackEffect(Stat(flat=1))
    thorns_effect = ThornsEffect(Stat(flat=3), duration=1)

    combat_manager.effect_manager.execute_effect(
        thorns_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 0,
        monster_0.hp == 100,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.THORNS).keyword == Keyword.THORNS,
        monster_1.get_effect(Keyword.THORNS).value == Stat(flat=3, percent=None),
        monster_1.get_effect(Keyword.THORNS).duration == 1,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_0,
        target=monster_1,
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 97,
            len(monster_1.effects) == 0,
            monster_1.get_effect(Keyword.THORNS) is None,
        ]
    )

    thorns_effect = ThornsEffect(Stat(percent=0.02), duration=1)

    combat_manager.effect_manager.execute_effect(
        thorns_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_0,
        target=monster_1,
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 95,
        ]
    )

    thorns_effect = ThornsEffect(Stat(flat=2, percent=0.03), duration=1)

    combat_manager.effect_manager.execute_effect(
        thorns_effect,
        source=monster_1,
        target=monster_1,
    )

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_0,
        target=monster_1,
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 90,
        ]
    )

    assert_conditions(conditions)
