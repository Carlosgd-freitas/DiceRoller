from colorama import init

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.combat.manager import CombatManager
from src.combat.team import Team
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.burn import BurnEffect
from src.effects.cleanse import CleanseEffect
from src.effects.confuse import ConfuseEffect
from src.effects.corrupt import CorruptEffect
from src.effects.curse import CurseEffect
from src.effects.doom import DoomEffect
from src.effects.drain import DrainEffect
from src.effects.execute import ExecuteEffect
from src.effects.focus import FocusEffect
from src.effects.freeze import FreezeEffect
from src.effects.heal import HealEffect
from src.effects.invisible import InvisibleEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.nothing import NothingEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.revive import ReviveEffect
from src.effects.sacred_block import SacredBlockEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from src.effects.thorns import ThornsEffect
from src.locales.languages import Language

init()

# ----------------------------

all_effects = [
    # Buffs
    FocusEffect(1),
    ManaRegenEffect(1),
    RegenEffect(1),
    ThornsEffect(1),
    # Debuff
    BleedEffect(1),
    BlindEffect(1),
    BurnEffect(1),
    ConfuseEffect(1),
    DoomEffect(1),
    FreezeEffect(1),
    PoisonEffect(1),
    SleepEffect(1),
    StunEffect(1),
    # Defensive
    AbsorbEffect(1),
    BlockEffect(1),
    InvisibleEffect(1),
    SacredBlockEffect(1),
    # Deterioration
    CorruptEffect(1),
    CurseEffect(1),
    ExecuteEffect(0.5),
    # Nothing
    NothingEffect(),
    # Offensive
    AttackEffect(1),
    DrainEffect(1),
    PierceEffect(1),
    # Restoration
    CleanseEffect(1),
    HealEffect(1),
    ManaEffect(1),
    ReviveEffect(0.25),
]

# ----------------------------

monster_a = Monster(
    name="Monster",
    hp=150,
    max_hp=200,
)

team_a = Team(
    name="Red Team",
    members=[monster_a],
)

monster_b = Monster(
    name="Monster",
    hp=150,
    max_hp=200,
)

team_b = Team(
    name="Blue Team",
    members=[monster_b],
)

# ----------------------------

combat_manager = CombatManager(
    teams=[
        team_a,
        team_b,
    ],
    order_strategy="SET",
    language=Language.EN_US,
)

combat_manager.start_combat()

# ----------------------------

print("===== Effect Execution: Target another alive monster =====")

for effect in all_effects:
    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_b,
    )

    monster_b.effects = []

# ----------------------------

print("\n===== Effect Execution: Target alive self =====")

for effect in all_effects:
    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_a,
    )

    monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: Target another dead monster =====")

for effect in all_effects:
    monster_b.hp = 0

    combat_manager.effect_manager.execute_effect(
        effect=effect, source=monster_a, target=monster_b
    )

    monster_b.effects = []

# ----------------------------

print("\n===== Effect Execution: Target dead self =====")

for effect in all_effects:
    monster_a.hp = 0

    combat_manager.effect_manager.execute_effect(
        effect=effect, source=monster_a, target=monster_a
    )

    monster_a.effects = []

monster_a.hp = 150
monster_b.hp = 150

# ----------------------------

print("\n===== Effect Execution: Target missing =====")

for effect in all_effects:
    monster_a.effects = [BlindEffect(1)]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_b,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: CLEANSE =====")

for effect in [
    CleanseEffect(0),
    CleanseEffect(1),
    CleanseEffect(2),
    CleanseEffect(5),
]:
    monster_a.effects = [
        BlindEffect(1),
        BurnEffect(1),
        PoisonEffect(1),
        BlindEffect(1),
        BurnEffect(1),
        PoisonEffect(1),
    ]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_a,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: CORRUPT =====")

for effect in [
    CorruptEffect(0),
    CorruptEffect(1),
    CorruptEffect(2),
    CorruptEffect(5),
]:
    monster_a.effects = [
        ManaRegenEffect(1),
        RegenEffect(1),
        ThornsEffect(1),
        ManaRegenEffect(1),
        RegenEffect(1),
        ThornsEffect(1),
    ]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_a,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: EXECUTE =====")

monster_b.hp = 100

combat_manager.effect_manager.execute_effect(
    effect=ExecuteEffect(0.5),
    source=monster_a,
    target=monster_b,
)

monster_b.hp = 150

# ----------------------------

print("\n===== Effect Removal =====")

removal_sets = [
    (
        BlindEffect(1),
        [FocusEffect(1)],
    ),
    (
        BurnEffect(1),
        [FreezeEffect(1)],
    ),
    (
        FocusEffect(1),
        [BlindEffect(1)],
    ),
    (
        FreezeEffect(1),
        [BurnEffect(1)],
    ),
    (
        SleepEffect(1),
        [
            AttackEffect(1),
            DrainEffect(1),
            PierceEffect(1),
        ],
    ),
]

for removed, removers in removal_sets:
    for remover in removers:
        monster_b.effects = [removed]

        combat_manager.effect_manager.execute_effect(
            effect=remover,
            source=monster_a,
            target=monster_b,
        )

# ----------------------------

print("\n===== Effect Activation: Act Disabling =====")

combat_manager.current_monster = monster_a

for effect in [
    FreezeEffect(1),
    SleepEffect(1),
    StunEffect(1),
]:
    monster_a.effects = [effect]

    combat_manager.take_turn()

monster_a.effects = []

# ----------------------------

print("\n===== Effect Activation: Being Attacked =====")

for effect in [
    AbsorbEffect(1),
    BlockEffect(1),
    InvisibleEffect(),
    SacredBlockEffect(1),
    ThornsEffect(1),
]:
    monster_b.effects = [effect]

    combat_manager.effect_manager.execute_effect(
        AttackEffect(2),
        source=monster_a,
        target=monster_b,
    )

monster_b.effects = []

# ----------------------------

print("\n===== Effect Activation: Dice Roll =====")

combat_manager.current_monster.dice = [
    Dice(sides=[Side(effects=[AttackEffect(1)])]),
]

for effect in [
    BleedEffect(1),
]:
    combat_manager.current_monster.effects = []
    combat_manager.current_monster.apply_effect(effect)

    combat_manager.start_turn()
    combat_manager.take_turn()

combat_manager.current_monster.dice = []

# ----------------------------

print("\n===== Effect Activation: Turn Start =====")

combat_manager.current_monster.effects = []

for effect in [
    BurnEffect(1),
    ManaRegenEffect(1),
    PoisonEffect(1),
    RegenEffect(1),
]:
    combat_manager.current_monster.apply_effect(effect)

combat_manager.start_turn()

# ----------------------------

print("\n===== Effect Activation: Turn End =====")

combat_manager.current_monster.effects = []

for effect in [
    DoomEffect(),
]:
    combat_manager.current_monster.apply_effect(effect)
    combat_manager.end_turn()

    combat_manager.current_monster.hp = 150

# ----------------------------

print("\n===== Effect Limit =====")

combat_manager.current_monster.effects = []

for i in range(10):
    if i % 2 == 0:
        effect = RegenEffect(value=1, duration=2)
    else:
        effect = InvisibleEffect(value=1, duration=2)

    combat_manager.current_monster.effects.append(effect)

combat_manager.logger.log_monster(combat_manager.current_monster)
