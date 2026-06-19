"""Tests for debuff effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
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
from src.effects.heal import HealEffect
from src.effects.poison import PoisonEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from src.effects.weak import WeakEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.manager import CombatManager
    from src.targeting.selectors.manager import SelectorManager


def test_keyword_bleed(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_2: Monster = managers["monsters"][2]
    monster_3: Monster = managers["monsters"][3]

    combat_manager.current_monster = monster_2

    effect_bleed = BleedEffect(1, duration=1)
    effect_attack_1 = AttackEffect(1)
    effect_attack_2 = AttackEffect(2)
    effect_attack_3 = AttackEffect(3)

    monster_2.dice = [
        Dice(sides=[Side([effect_attack_1])]),
        Dice(sides=[Side([effect_attack_2])]),
        Dice(sides=[Side([effect_attack_3])]),
    ]

    combat_manager.effect_manager.execute_effect(
        effect_bleed,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.BLEED).keyword == Keyword.BLEED,
        monster_2.get_effect(Keyword.BLEED).value == 1,
        monster_2.get_effect(Keyword.BLEED).duration == 1,
        monster_2.hp == 10,
        monster_3.local_id == "MONSTER_3",
        len(monster_3.effects) == 0,
        monster_3.get_effect(Keyword.BLEED) is None,
        monster_3.hp == 100,
    ]

    rolled = combat_manager.effect_manager.roll(monster_2)

    conditions.extend(
        [
            len(rolled) == 3,
            rolled[0].effects[0].value == 1,
            rolled[1].effects[0].value == 2,
            rolled[2].effects[0].value == 3,
            monster_2.hp == 7,
            monster_3.hp == 100,
        ]
    )

    combat_manager.end_turn()

    rolled = monster_3.roll()

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.BLEED) is None,
            monster_2.hp == 7,
            monster_3.hp == 100,
        ]
    )

    assert_conditions(conditions)


def test_keyword_blind(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    effect_blind = BlindEffect(1, duration=1)
    effect_focus = FocusEffect(1, duration=1)
    effect_heal = HealEffect(2)
    effect_attack = AttackEffect(2)

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
        monster_1.get_effect(Keyword.BLIND).value == 1,
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


def test_keyword_burn(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    combat_manager.current_monster = monster_2

    effect_burn = BurnEffect(2)
    effect_freeze = FreezeEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_burn,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.BURN).keyword == Keyword.BURN,
        monster_2.get_effect(Keyword.BURN).value == 2,
        monster_2.get_effect(Keyword.BURN).duration == 1,
        monster_2.hp == 10,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.get_effect(Keyword.BURN) is None,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.effect_manager.execute_effect(
        effect_freeze,
        source=monster_2,
        target=monster_2,
    )

    conditions.extend(
        [
            len(monster_2.effects) == 1,
            monster_2.get_effect(Keyword.BURN) is None,
            monster_2.get_effect(Keyword.FREEZE).keyword == Keyword.FREEZE,
            monster_2.hp == 8,
            monster_1.hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_confuse(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector_manager: SelectorManager = managers["selector_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]
    monster_3: Monster = managers["monsters"][3]

    effect_confuse = ConfuseEffect(duration=1)
    effect_attack = AttackEffect(1)
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


def test_keyword_doom(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

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


def test_keyword_fragile(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]

    combat_manager.current_monster = monster_1

    block_effect = BlockEffect(3, duration=1)
    fragile_effect = FragileEffect(2, duration=1)

    combat_manager.effect_manager.execute_effect(
        fragile_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.FRAGILE).keyword == Keyword.FRAGILE,
        monster_1.get_effect(Keyword.FRAGILE).value == 2,
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
            monster_1.get_effect(Keyword.BLOCK).value == 1,
            monster_1.get_effect(Keyword.BLOCK).duration == 1,
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
            len(monster_1.effects) == 1,
            monster_1.get_effect(Keyword.FRAGILE) is None,
            monster_1.get_effect(Keyword.BLOCK).keyword == Keyword.BLOCK,
            monster_1.get_effect(Keyword.BLOCK).value == 3,
            monster_1.get_effect(Keyword.BLOCK).duration == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_freeze(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]
    monster_3: Monster = managers["monsters"][3]

    effect_freeze = FreezeEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)
    effect_burn = BurnEffect(2, duration=1)

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


def test_keyword_frostburn(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    combat_manager.current_monster = monster_2

    effect_frostburn = FrostburnEffect(2, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_frostburn,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.FROSTBURN).keyword == Keyword.FROSTBURN,
        monster_2.get_effect(Keyword.FROSTBURN).value == 2,
        monster_2.get_effect(Keyword.FROSTBURN).duration == 1,
        monster_2.hp == 10,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.get_effect(Keyword.FROSTBURN) is None,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.FROSTBURN) is None,
            monster_2.hp == 8,
            monster_1.hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_poison(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    combat_manager.current_monster = monster_2

    effect_poison = PoisonEffect(3, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_poison,
        source=monster_2,
        target=monster_2,
    )

    conditions = [
        monster_2.local_id == "MONSTER_2",
        len(monster_2.effects) == 1,
        monster_2.get_effect(Keyword.POISON).keyword == Keyword.POISON,
        monster_2.get_effect(Keyword.POISON).value == 3,
        monster_2.get_effect(Keyword.POISON).duration == 1,
        monster_2.hp == 10,
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 0,
        monster_1.get_effect(Keyword.POISON) is None,
        monster_1.hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(monster_2.effects) == 0,
            monster_2.get_effect(Keyword.POISON) is None,
            monster_2.hp == 7,
            monster_1.hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_sleep(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_2: Monster = managers["monsters"][2]
    monster_3: Monster = managers["monsters"][3]

    combat_manager.current_monster = monster_2

    effect_sleep = SleepEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

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


def test_keyword_stun(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_2: Monster = managers["monsters"][2]

    effect_stun = StunEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

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


def test_keyword_weak(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    monster_1: Monster = managers["monsters"][1]
    monster_3: Monster = managers["monsters"][3]

    combat_manager.current_monster = monster_1

    attack_effect = AttackEffect(2)
    weak_effect = WeakEffect(2, duration=1)

    combat_manager.effect_manager.execute_effect(
        weak_effect,
        source=monster_1,
        target=monster_1,
    )

    conditions = [
        monster_1.local_id == "MONSTER_1",
        len(monster_1.effects) == 1,
        monster_1.get_effect(Keyword.WEAK).keyword == Keyword.WEAK,
        monster_1.get_effect(Keyword.WEAK).value == 2,
        monster_1.get_effect(Keyword.WEAK).duration == 1,
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
            monster_1.hp == 1,
            len(monster_1.effects) == 1,
            monster_1.get_effect(Keyword.WEAK).keyword == Keyword.WEAK,
            monster_1.get_effect(Keyword.WEAK).value == 2,
            monster_1.get_effect(Keyword.WEAK).duration == 1,
            monster_3.hp == 100,
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
            monster_3.hp == 98,
        ]
    )

    assert_conditions(conditions)
