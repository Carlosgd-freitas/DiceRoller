"""Tests for debuff effects processing."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
from src.base.stat import Stat
from src.combat.manager import CombatManager
from src.combat.order_strategy import OrderStrategy
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.burn import BurnEffect
from src.effects.confuse import ConfuseEffect
from src.effects.doom import DoomEffect
from src.effects.focus import FocusEffect
from src.effects.fragile import FragileEffect
from src.effects.freeze import FreezeEffect
from src.effects.frostburn import FrostburnEffect
from src.effects.haste import HasteEffect
from src.effects.heal import HealEffect
from src.effects.oil import OilEffect
from src.effects.poison import PoisonEffect
from src.effects.sleep import SleepEffect
from src.effects.slow import SlowEffect
from src.effects.stun import StunEffect
from src.effects.weak import WeakEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.systems.targeting.selectors.manager import SelectorManager


def test_bleed_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    side = Side(effects=[AttackEffect()])
    monster_0.dice = [
        Dice(sides=[deepcopy(side)]),
        Dice(sides=[deepcopy(side)]),
        Dice(sides=[deepcopy(side)]),
    ]
    monster_0.hp = 100

    combat_manager.current_monster = monster_0

    effect = BleedEffect(Stat(flat=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 1,
        monster_0.get_effect(Keyword.BLEED).keyword == Keyword.BLEED,
        monster_0.get_effect(Keyword.BLEED).value == Stat(flat=2, percent=None),
        monster_0.get_effect(Keyword.BLEED).duration == 1,
        monster_0.hp == 100,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.hp == 1,
    ]

    combat_manager.effect_manager.roll(monster_0)
    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_0.effects) == 0,
            monster_0.get_effect(Keyword.BLEED) is None,
            monster_0.hp == 94,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = BleedEffect(Stat(percent=0.01), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.effect_manager.roll(monster_0)
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 91,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = BleedEffect(Stat(flat=2, percent=0.03), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.effect_manager.roll(monster_0)
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 76,
        ]
    )

    assert_conditions(conditions)


def test_blind_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect_blind = BlindEffect(Stat(percent=1), duration=1)
    effect_focus = FocusEffect(Stat(percent=1), duration=1)
    effect_heal = HealEffect(Stat(flat=2))
    effect_attack = AttackEffect(Stat(flat=2))

    combat_manager.effect_manager.execute_effect(
        effect_focus,
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
        monster_1.get_effect(Keyword.FOCUS) is None,
        monster_1.get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
        monster_1.get_effect(Keyword.BLIND).value == Stat(flat=None, percent=1),
        monster_1.get_effect(Keyword.BLIND).duration == 1,
        monster_1.hp == 1,
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 0,
        monster_2.get_effect(Keyword.BLIND) is None,
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
            monster_2.hp == 10,
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
            monster_1.get_effect(Keyword.BLIND) is None,
            monster_1.hp == 5,
            monster_2.hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_burn_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    monster_0.hp = 100
    combat_manager.current_monster = monster_0

    burn_effect = BurnEffect(Stat(flat=2), duration=1)
    freeze_effect = FreezeEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        freeze_effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.effect_manager.execute_effect(
        burn_effect,
        source=monster_1,
        target=monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 1,
        monster_0.get_effect(Keyword.BURN).keyword == Keyword.BURN,
        monster_0.get_effect(Keyword.BURN).value == Stat(flat=2, percent=None),
        monster_0.get_effect(Keyword.BURN).duration == 1,
        monster_0.hp == 100,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_0.effects) == 0,
            monster_0.get_effect(Keyword.BURN) is None,
            monster_0.hp == 98,
        ]
    )

    combat_manager.current_monster = monster_0

    burn_effect = BurnEffect(Stat(percent=0.01), duration=1)

    combat_manager.effect_manager.execute_effect(
        burn_effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 97,
        ]
    )

    combat_manager.current_monster = monster_0

    burn_effect = BurnEffect(Stat(flat=3, percent=0.04), duration=1)

    combat_manager.effect_manager.execute_effect(
        burn_effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 90,
        ]
    )

    assert_conditions(conditions)


def test_confuse_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    selector_manager: SelectorManager = combat["selector_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]

    effect_confuse = ConfuseEffect(Stat(percent=1), duration=1)
    effect_attack = AttackEffect(Stat(flat=1))
    side = Side(effects=[effect_attack])

    combat_manager.effect_manager.execute_effect(
        effect_confuse,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.CONFUSE).keyword == Keyword.CONFUSE,
        monster_1.get_effect(Keyword.CONFUSE).value == Stat(flat=None, percent=1),
        monster_1.get_effect(Keyword.CONFUSE).duration == 1,
        monster_1.hp == 1,
    ]

    targets: List[Monster] = selector_manager.get_targets(
        side=side,
        source=monster_1,
        allies=[monster_2],
        enemies=[monster_3],
    )

    conditions.extend(
        [
            len(targets) == 1,
            targets[0].local_id in ["MONSTER_1", "MONSTER_2", "MONSTER_3"],
        ]
    )

    combat_manager.end_turn()

    targets: List[Monster] = selector_manager.get_targets(
        side=side,
        source=monster_1,
        allies=[monster_2],
        enemies=[monster_3],
    )

    conditions.extend(
        [
            len(targets) == 1,
            targets[0].local_id == "MONSTER_3",
        ]
    )

    assert_conditions(conditions)


def test_doom_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect_doom = DoomEffect(duration=3)

    combat_manager.effect_manager.execute_effect(
        effect_doom,
        source=monster_2,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
        monster_1.get_effect(Keyword.DOOM).duration == 3,
        monster_1.is_alive(),
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 0,
        monster_2.get_effect(Keyword.DOOM) is None,
        monster_2.is_alive(),
    ]

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_1.get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
            monster_1.get_effect(Keyword.DOOM).duration == 2,
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_1.get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
            monster_1.get_effect(Keyword.DOOM).duration == 1,
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            monster_1.get_effect(Keyword.DOOM) is None,
            not monster_1.is_alive(),
        ]
    )

    assert_conditions(conditions)


def test_fragile_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]

    block_effect = BlockEffect(Stat(flat=6), duration=1)
    fragile_effect = FragileEffect(Stat(flat=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        fragile_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.FRAGILE).keyword == Keyword.FRAGILE,
        monster_1.get_effect(Keyword.FRAGILE).value == Stat(flat=2, percent=None),
        monster_1.get_effect(Keyword.FRAGILE).duration == 1,
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
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=4, percent=None),
            monster_1.get_effect(Keyword.BLOCK).duration == 1,
        ]
    )

    combat_manager.end_turn()

    monster_1.effects = []

    fragile_effect = FragileEffect(Stat(percent=0.5), duration=1)

    combat_manager.effect_manager.execute_effect(
        fragile_effect,
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
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=3, percent=None),
        ]
    )

    combat_manager.end_turn()

    monster_1.effects = []

    fragile_effect = FragileEffect(Stat(flat=2, percent=0.5), duration=1)

    combat_manager.effect_manager.execute_effect(
        fragile_effect,
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
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=2, percent=None),
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
            monster_1.get_effect(Keyword.BLOCK).value == Stat(flat=6, percent=None),
        ]
    )

    assert_conditions(conditions)


def test_freeze_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]

    effect_freeze = FreezeEffect(duration=1)
    effect_attack = AttackEffect(Stat(flat=2))
    effect_heal = HealEffect(Stat(flat=2))
    effect_burn = BurnEffect(Stat(flat=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_freeze,
        source=monster_1,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.FREEZE).keyword == Keyword.FREEZE,
        monster_2.get_effect(Keyword.FREEZE).duration == 1,
        monster_2.hp == 10,
        monster_3.local_id == "MONSTER_3",
        len(monster_3.effects) == 0,
        monster_3.get_effect(Keyword.FREEZE) is None,
        monster_3.hp == 100,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_2,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_2,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_3.hp == 100,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_burn,
        source=monster_1,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_2,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_2,
        target=monster_3,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 1,
            monster_2.get_effect(Keyword.FREEZE) is None,
            monster_2.get_effect(Keyword.BURN).keyword == Keyword.BURN,
            monster_2.hp == 12,
            monster_3.hp == 98,
        ]
    )

    assert_conditions(conditions)


def test_frostburn_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    monster_0.hp = 100
    combat_manager.current_monster = monster_0

    effect = FrostburnEffect(Stat(flat=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 1,
        monster_0.get_effect(Keyword.FROSTBURN).keyword == Keyword.FROSTBURN,
        monster_0.get_effect(Keyword.FROSTBURN).value == Stat(flat=2, percent=None),
        monster_0.get_effect(Keyword.FROSTBURN).duration == 1,
        monster_0.hp == 100,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_0.effects) == 0,
            monster_0.get_effect(Keyword.FROSTBURN) is None,
            monster_0.hp == 98,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = FrostburnEffect(Stat(percent=0.01), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 97,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = FrostburnEffect(Stat(flat=3, percent=0.04), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 90,
        ]
    )

    assert_conditions(conditions)


def test_oil_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.order_strategy = OrderStrategy.FASTER
    combat_manager.start_combat()

    turn_local_ids = []

    combat_manager.start_round()
    for turn in range(4):
        combat_manager.start_turn()
        turn_local_ids.append(combat_manager.current_monster.local_id)

        if turn == 0:
            oil_effect = OilEffect(Stat(flat=5), duration=1)

            combat_manager.effect_manager.execute_effect(
                oil_effect,
                source=combat_manager.current_monster,
                target=monster_2,
            )

            burn_effect = BurnEffect(Stat(flat=1), duration=1)

            combat_manager.effect_manager.execute_effect(
                burn_effect,
                source=combat_manager.current_monster,
                target=monster_2,
            )

            conditions = [
                monster_2.local_id == "MONSTER_2",
                len(monster_2.effects) == 2,
                monster_2.hp == 10,
                monster_2.get_effect(Keyword.OIL).keyword == Keyword.OIL,
                monster_2.get_effect(Keyword.OIL).value == Stat(flat=5),
                monster_2.get_effect(Keyword.OIL).duration == 1,
                monster_2.speed == 1,
                monster_2.get_effective_speed() == -4,
            ]

        combat_manager.current_monster.turn_taken = True
        combat_manager.end_turn()
        combat_manager.next_turn()
    combat_manager.end_round()

    conditions.extend(
        [
            turn_local_ids[0] == "MONSTER_3",
            turn_local_ids[1] == "MONSTER_1",
            turn_local_ids[2] == "MONSTER_4",
            turn_local_ids[3] == "MONSTER_2",
            len(monster_2.effects) == 0,
            monster_2.hp == 4,
            monster_2.get_effect(Keyword.OIL) is None,
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

    haste_effect = HasteEffect(Stat(flat=100), duration=1)
    oil_effect = OilEffect(Stat(percent=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        haste_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        oil_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == -1,
        ]
    )

    monster_2.effects = []

    oil_effect = OilEffect(Stat(flat=2, percent=2), duration=1)

    combat_manager.effect_manager.execute_effect(
        oil_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == -3,
        ]
    )

    assert_conditions(conditions)


def test_poison_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_0: Monster = combat["monsters"][0]
    monster_1: Monster = combat["monsters"][1]

    monster_0.hp = 100
    combat_manager.current_monster = monster_0

    effect = PoisonEffect(Stat(flat=3), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    conditions = [
        monster_0.local_id == "MONSTER_0",
        len(monster_0.effects) == 1,
        monster_0.get_effect(Keyword.POISON).keyword == Keyword.POISON,
        monster_0.get_effect(Keyword.POISON).value == Stat(flat=3, percent=None),
        monster_0.get_effect(Keyword.POISON).duration == 1,
        monster_0.hp == 100,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_0.effects) == 0,
            monster_0.get_effect(Keyword.POISON) is None,
            monster_0.hp == 97,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = PoisonEffect(Stat(percent=0.02), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 95,
        ]
    )

    combat_manager.current_monster = monster_0

    effect = PoisonEffect(Stat(flat=2, percent=0.03), duration=1)

    combat_manager.effect_manager.execute_effect(
        effect,
        source=monster_1,
        target=monster_0,
    )

    combat_manager.start_turn()
    combat_manager.end_turn()

    conditions.extend(
        [
            monster_0.hp == 90,
        ]
    )

    assert_conditions(conditions)


def test_sleep_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_2: Monster = combat["monsters"][2]
    monster_3: Monster = combat["monsters"][3]

    combat_manager.current_monster = monster_2

    effect_sleep = SleepEffect(duration=1)
    effect_attack = AttackEffect(Stat(flat=2))
    effect_heal = HealEffect(Stat(flat=2))

    combat_manager.effect_manager.execute_effect(
        effect_sleep,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.SLEEP).keyword == Keyword.SLEEP,
        monster_2.get_effect(Keyword.SLEEP).duration == 1,
        monster_2.hp == 10,
        monster_3.local_id == "MONSTER_3",
        len(monster_3.effects) == 0,
        monster_3.get_effect(Keyword.SLEEP) is None,
        monster_3.hp == 100,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_2,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_2,
        target=monster_3,
    )

    conditions.extend(
        [
            monster_2.hp == 10,
            monster_3.hp == 100,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_3,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.SLEEP) is None,
            monster_2.hp == 8,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=monster_2,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=monster_2,
        target=monster_3,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.SLEEP) is None,
            monster_2.hp == 10,
            monster_3.hp == 98,
        ]
    )

    assert_conditions(conditions)


def test_slow_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_2: Monster = combat["monsters"][2]

    combat_manager.order_strategy = OrderStrategy.FASTER
    combat_manager.start_combat()

    turn_local_ids = []

    combat_manager.start_round()
    for turn in range(4):
        turn_local_ids.append(combat_manager.current_monster.local_id)

        if turn == 0:
            slow_effect = SlowEffect(Stat(flat=100), duration=1)

            combat_manager.effect_manager.execute_effect(
                slow_effect,
                source=combat_manager.current_monster,
                target=monster_2,
            )

            conditions = [
                monster_2.local_id == "MONSTER_2",
                len(monster_2.effects) == 1,
                monster_2.get_effect(Keyword.SLOW).keyword == Keyword.SLOW,
                monster_2.get_effect(Keyword.SLOW).value == Stat(flat=100),
                monster_2.get_effect(Keyword.SLOW).duration == 1,
                monster_2.speed == 1,
                monster_2.get_effective_speed() == -99,
            ]

        combat_manager.current_monster.turn_taken = True
        combat_manager.end_turn()
        combat_manager.next_turn()
    combat_manager.end_round()

    conditions.extend(
        [
            turn_local_ids[0] == "MONSTER_3",
            turn_local_ids[1] == "MONSTER_1",
            turn_local_ids[2] == "MONSTER_4",
            turn_local_ids[3] == "MONSTER_2",
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.SLOW) is None,
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

    haste_effect = HasteEffect(Stat(flat=100), duration=1)
    slow_effect = SlowEffect(Stat(percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        haste_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    combat_manager.effect_manager.execute_effect(
        slow_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == 0,
        ]
    )

    monster_2.effects = []

    slow_effect = SlowEffect(Stat(flat=2, percent=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        slow_effect,
        source=combat_manager.current_monster,
        target=monster_2,
    )

    conditions.extend(
        [
            monster_2.speed == 1,
            monster_2.get_effective_speed() == -2,
        ]
    )

    assert_conditions(conditions)


def test_stun_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_2: Monster = combat["monsters"][2]

    effect_stun = StunEffect(duration=1)
    effect_attack = AttackEffect(Stat(flat=2))
    effect_heal = HealEffect(Stat(flat=2))

    combat_manager.effect_manager.execute_effect(
        effect_stun,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.STUN).keyword == Keyword.STUN,
        monster_1.get_effect(Keyword.STUN).duration == 1,
        monster_1.hp == 1,
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 0,
        monster_2.get_effect(Keyword.STUN) is None,
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
            monster_1.hp == 1,
            monster_2.hp == 10,
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
            monster_1.get_effect(Keyword.STUN) is None,
            monster_1.hp == 3,
            monster_2.hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_weak_effect(combat: Dict):
    combat_manager: CombatManager = combat["combat_manager"]
    monster_1: Monster = combat["monsters"][1]
    monster_3: Monster = combat["monsters"][3]

    attack_effect = AttackEffect(Stat(flat=4))
    weak_effect = WeakEffect(Stat(flat=1), duration=1)

    combat_manager.effect_manager.execute_effect(
        weak_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        monster_1.hp == 1,
        len(monster_1.effects) == 1,
        monster_3.local_id == "MONSTER_3",
        monster_3.get_effect(Keyword.WEAK) is None,
    ]

    combat_manager.effect_manager.execute_effect(
        attack_effect,
        source=monster_1,
        target=monster_3,
    )

    conditions.extend(
        [
            len(monster_1.effects) == 1,
            monster_1.get_effect(Keyword.WEAK).keyword == Keyword.WEAK,
            monster_1.get_effect(Keyword.WEAK).value == Stat(flat=1, percent=None),
            monster_1.get_effect(Keyword.WEAK).duration == 1,
            monster_3.hp == 97,
        ]
    )

    combat_manager.end_turn()

    weak_effect = WeakEffect(Stat(percent=0.5), duration=1)

    combat_manager.effect_manager.execute_effect(
        weak_effect,
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
            monster_3.hp == 95,
        ]
    )

    combat_manager.end_turn()

    weak_effect = WeakEffect(Stat(flat=2, percent=0.5), duration=1)

    combat_manager.effect_manager.execute_effect(
        weak_effect,
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
            monster_3.hp == 94,
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
            monster_1.get_effect(Keyword.WEAK) is None,
            monster_3.hp == 90,
        ]
    )

    combat_manager.end_turn()

    assert_conditions(conditions)
