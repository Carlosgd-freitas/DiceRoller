"""Tests for debuff effects processing."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List

from src.base.dice import Dice
from src.base.keywords import Keyword
from src.base.side import Side
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.burn import BurnEffect
from src.effects.confuse import ConfuseEffect
from src.effects.doom import DoomEffect
from src.effects.focus import FocusEffect
from src.effects.freeze import FreezeEffect
from src.effects.frostburn import FrostburnEffect
from src.effects.heal import HealEffect
from src.effects.poison import PoisonEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from tests.utils import assert_conditions

if TYPE_CHECKING:
    from src.base.monster import Monster
    from src.combat.manager import CombatManager
    from src.targeting.selectors.manager import SelectorManager


def test_keyword_bleed(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect_bleed = BleedEffect(1, duration=1)
    effect_attack_1 = AttackEffect(1)
    effect_attack_2 = AttackEffect(2)
    effect_attack_3 = AttackEffect(3)

    combat_manager.order[1].dice = [
        Dice(sides=[Side([effect_attack_1])]),
        Dice(sides=[Side([effect_attack_2])]),
        Dice(sides=[Side([effect_attack_3])]),
    ]

    combat_manager.effect_manager.execute_effect(
        effect_bleed,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.BLEED).keyword == Keyword.BLEED,
        combat_manager.order[1].get_effect(Keyword.BLEED).value == 1,
        combat_manager.order[1].get_effect(Keyword.BLEED).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[2].local_id == "MONSTER_3",
        len(combat_manager.order[2].effects) == 0,
        combat_manager.order[2].get_effect(Keyword.BLEED) is None,
        combat_manager.order[2].hp == 100,
    ]

    rolled = combat_manager.effect_manager.roll(combat_manager.order[1])

    conditions.extend(
        [
            len(rolled) == 3,
            rolled[0].effects[0].value == 1,
            rolled[1].effects[0].value == 2,
            rolled[2].effects[0].value == 3,
            combat_manager.order[1].hp == 7,
            combat_manager.order[2].hp == 100,
        ]
    )

    combat_manager.end_turn()

    rolled = combat_manager.order[2].roll()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.BLEED) is None,
            combat_manager.order[1].hp == 7,
            combat_manager.order[2].hp == 100,
        ]
    )

    assert_conditions(conditions)


def test_keyword_blind(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_blind = BlindEffect(1, duration=1)
    effect_focus = FocusEffect(1, duration=1)
    effect_heal = HealEffect(2)
    effect_attack = AttackEffect(2)

    combat_manager.effect_manager.execute_effect(
        effect_focus,
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
        combat_manager.order[0].get_effect(Keyword.FOCUS) is None,
        combat_manager.order[0].get_effect(Keyword.BLIND).keyword == Keyword.BLIND,
        combat_manager.order[0].get_effect(Keyword.BLIND).value == 1,
        combat_manager.order[0].get_effect(Keyword.BLIND).duration == 1,
        combat_manager.order[0].hp == 1,
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.BLIND) is None,
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
            combat_manager.order[1].hp == 10,
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
            combat_manager.order[0].get_effect(Keyword.BLIND) is None,
            combat_manager.order[0].hp == 5,
            combat_manager.order[1].hp == 8,
        ]
    )

    assert_conditions(conditions)


def test_keyword_burn(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect_burn = BurnEffect(2)
    effect_freeze = FreezeEffect(duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_burn,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.BURN).keyword == Keyword.BURN,
        combat_manager.order[1].get_effect(Keyword.BURN).value == 2,
        combat_manager.order[1].get_effect(Keyword.BURN).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.BURN) is None,
        combat_manager.order[0].hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.effect_manager.execute_effect(
        effect_freeze,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 1,
            combat_manager.order[1].get_effect(Keyword.BURN) is None,
            combat_manager.order[1].get_effect(Keyword.FREEZE).keyword
            == Keyword.FREEZE,
            combat_manager.order[1].hp == 8,
            combat_manager.order[0].hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_confuse(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]
    selector_manager: SelectorManager = managers["selector_manager"]

    effect_confuse = ConfuseEffect(duration=1)
    effect_attack = AttackEffect(1)
    side = Side(effects=[effect_attack])

    combat_manager.effect_manager.execute_effect(
        effect_confuse,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.CONFUSE).keyword == Keyword.CONFUSE,
        combat_manager.order[0].get_effect(Keyword.CONFUSE).duration == 1,
        combat_manager.order[0].hp == 1,
    ]

    targets: List[Monster] = selector_manager.get_targets(
        side=side,
        source=combat_manager.order[0],
        allies=[combat_manager.order[1]],
        enemies=[combat_manager.order[2]],
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
        source=combat_manager.order[0],
        allies=[combat_manager.order[1]],
        enemies=[combat_manager.order[2]],
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

    effect_doom = DoomEffect(duration=3)

    combat_manager.effect_manager.execute_effect(
        effect_doom,
        source=combat_manager.order[1],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
        combat_manager.order[0].get_effect(Keyword.DOOM).duration == 3,
        combat_manager.order[0].is_alive(),
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.DOOM) is None,
        combat_manager.order[1].is_alive(),
    ]

    combat_manager.end_turn()

    conditions.extend(
        [
            combat_manager.order[0].get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
            combat_manager.order[0].get_effect(Keyword.DOOM).duration == 2,
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            combat_manager.order[0].get_effect(Keyword.DOOM).keyword == Keyword.DOOM,
            combat_manager.order[0].get_effect(Keyword.DOOM).duration == 1,
        ]
    )

    combat_manager.end_turn()

    conditions.extend(
        [
            combat_manager.order[0].get_effect(Keyword.DOOM) is None,
            not combat_manager.order[0].is_alive(),
        ]
    )

    assert_conditions(conditions)


def test_keyword_freeze(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_freeze = FreezeEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)
    effect_burn = BurnEffect(2, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_freeze,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.FREEZE).keyword == Keyword.FREEZE,
        combat_manager.order[1].get_effect(Keyword.FREEZE).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[2].local_id == "MONSTER_3",
        len(combat_manager.order[2].effects) == 0,
        combat_manager.order[2].get_effect(Keyword.FREEZE) is None,
        combat_manager.order[2].hp == 100,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            combat_manager.order[1].hp == 10,
            combat_manager.order[2].hp == 100,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_burn,
        source=combat_manager.order[0],
        target=combat_manager.order[1],
    )

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 1,
            combat_manager.order[1].get_effect(Keyword.FREEZE) is None,
            combat_manager.order[1].get_effect(Keyword.BURN).keyword == Keyword.BURN,
            combat_manager.order[1].hp == 12,
            combat_manager.order[2].hp == 98,
        ]
    )

    assert_conditions(conditions)


def test_keyword_frostburn(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect_frostburn = FrostburnEffect(2, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_frostburn,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.FROSTBURN).keyword
        == Keyword.FROSTBURN,
        combat_manager.order[1].get_effect(Keyword.FROSTBURN).value == 2,
        combat_manager.order[1].get_effect(Keyword.FROSTBURN).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.FROSTBURN) is None,
        combat_manager.order[0].hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.FROSTBURN) is None,
            combat_manager.order[1].hp == 8,
            combat_manager.order[0].hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_poison(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect_poison = PoisonEffect(3, duration=1)

    combat_manager.effect_manager.execute_effect(
        effect_poison,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.POISON).keyword == Keyword.POISON,
        combat_manager.order[1].get_effect(Keyword.POISON).value == 3,
        combat_manager.order[1].get_effect(Keyword.POISON).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 0,
        combat_manager.order[0].get_effect(Keyword.POISON) is None,
        combat_manager.order[0].hp == 1,
    ]

    combat_manager.start_turn()

    combat_manager.end_turn()

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.POISON) is None,
            combat_manager.order[1].hp == 7,
            combat_manager.order[0].hp == 1,
        ]
    )

    assert_conditions(conditions)


def test_keyword_sleep(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    combat_manager.current_monster = combat_manager.order[1]

    effect_sleep = SleepEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

    combat_manager.effect_manager.execute_effect(
        effect_sleep,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    conditions = [
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 1,
        combat_manager.order[1].get_effect(Keyword.SLEEP).keyword == Keyword.SLEEP,
        combat_manager.order[1].get_effect(Keyword.SLEEP).duration == 1,
        combat_manager.order[1].hp == 10,
        combat_manager.order[2].local_id == "MONSTER_3",
        len(combat_manager.order[2].effects) == 0,
        combat_manager.order[2].get_effect(Keyword.SLEEP) is None,
        combat_manager.order[2].hp == 100,
    ]

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            combat_manager.order[1].hp == 10,
            combat_manager.order[2].hp == 100,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[2],
        target=combat_manager.order[1],
    )

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.SLEEP) is None,
            combat_manager.order[1].hp == 8,
        ]
    )

    combat_manager.effect_manager.execute_effect(
        effect_heal,
        source=combat_manager.order[1],
        target=combat_manager.order[1],
    )

    combat_manager.effect_manager.execute_effect(
        effect_attack,
        source=combat_manager.order[1],
        target=combat_manager.order[2],
    )

    conditions.extend(
        [
            len(combat_manager.order[1].effects) == 0,
            combat_manager.order[1].get_effect(Keyword.SLEEP) is None,
            combat_manager.order[1].hp == 10,
            combat_manager.order[2].hp == 98,
        ]
    )

    assert_conditions(conditions)


def test_keyword_stun(managers: Dict):
    combat_manager: CombatManager = managers["combat_manager"]

    effect_stun = StunEffect(duration=1)
    effect_attack = AttackEffect(2)
    effect_heal = HealEffect(2)

    combat_manager.effect_manager.execute_effect(
        effect_stun,
        source=combat_manager.order[0],
        target=combat_manager.order[0],
    )

    conditions = [
        combat_manager.order[0].local_id == "MONSTER_1",
        len(combat_manager.order[0].effects) == 1,
        combat_manager.order[0].get_effect(Keyword.STUN).keyword == Keyword.STUN,
        combat_manager.order[0].get_effect(Keyword.STUN).duration == 1,
        combat_manager.order[0].hp == 1,
        combat_manager.order[1].local_id == "MONSTER_2",
        len(combat_manager.order[1].effects) == 0,
        combat_manager.order[1].get_effect(Keyword.STUN) is None,
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
            combat_manager.order[0].hp == 1,
            combat_manager.order[1].hp == 10,
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
            combat_manager.order[0].get_effect(Keyword.STUN) is None,
            combat_manager.order[0].hp == 3,
            combat_manager.order[1].hp == 8,
        ]
    )

    assert_conditions(conditions)
