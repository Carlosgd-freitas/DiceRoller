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
from src.effects.confuse import ConfuseEffect
from src.effects.curse import CurseEffect
from src.effects.drain import DrainEffect
from src.effects.freeze import FreezeEffect
from src.effects.heal import HealEffect
from src.effects.mana import ManaEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.nothing import NothingEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.sleep import SleepEffect
from src.effects.stun import StunEffect
from src.effects.thorns import ThornsEffect

init()

# ----------------------------

buff_effects = [
    ManaRegenEffect(1),
    RegenEffect(1),
    ThornsEffect(1),
]

curse_effects = [
    CurseEffect(1),
]

debuff_effects = [
    BleedEffect(1),
    BlindEffect(1),
    BurnEffect(1),
    ConfuseEffect(1),
    FreezeEffect(1),
    PoisonEffect(1),
    SleepEffect(1),
    StunEffect(1),
]

defensive_effects = [
    AbsorbEffect(1),
    BlockEffect(1),
]

nothing_effects = [
    NothingEffect(1),
]

offensive_effects = [
    AttackEffect(1),
    DrainEffect(1),
    PierceEffect(1),
]

restoration_effects = [
    HealEffect(1),
    ManaEffect(1),
]

# ----------------------------

monster_a = Monster(
    name="Monster",
    hp=100,
    max_hp=200,
    dice=[
        Dice(sides=[Side(effects=buff_effects)]),
        Dice(sides=[Side(effects=curse_effects)]),
        Dice(sides=[Side(effects=debuff_effects)]),
        Dice(sides=[Side(effects=defensive_effects)]),
        Dice(sides=[Side(effects=nothing_effects)]),
        Dice(sides=[Side(effects=offensive_effects)]),
        Dice(sides=[Side(effects=restoration_effects)]),
    ],
)

team_a = Team(
    name="Red Team",
    members=[monster_a],
)

monster_b = Monster(
    name="Monster",
    hp=100,
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
    language="EN-US",
)

# ----------------------------

print("===== Effect Execution =====")

combat_manager.start_combat()

combat_manager.logger.log(message="\n[Start Combat]")
combat_manager.logger.log_monster(combat_manager.order[0])
combat_manager.logger.log_monster(combat_manager.order[1])

# ----

combat_manager.start_turn()

combat_manager.logger.log(message="\n[Start Turn]")
combat_manager.logger.log_monster(combat_manager.order[0])
combat_manager.logger.log_monster(combat_manager.order[1])
combat_manager.logger.log(message="")

# ----

combat_manager.take_turn()

combat_manager.logger.log(message="\n[Take Turn]")
combat_manager.logger.log_monster(combat_manager.order[0])
combat_manager.logger.log_monster(combat_manager.order[1])

# ----

combat_manager.end_turn()

combat_manager.logger.log(message="\n[End Turn]")
combat_manager.logger.log_monster(combat_manager.order[0])
combat_manager.logger.log_monster(combat_manager.order[1])

# ----

combat_manager.current_monster.effects = []

combat_manager.next_turn()
combat_manager.current_monster.effects = []

# ----------------------------

print("\n===== Effect Removal =====")

removal_sets = [
    (
        BurnEffect(1),
        [FreezeEffect(1)],
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
        combat_manager.current_monster.effects = [removed]

        combat_manager.effect_manager.execute_effect(
            effect=remover,
            source=monster_a,
            target=monster_b,
        )

# ----------------------------

print("\n===== Effect Activation: Act Disabling =====")

for effect in [
    FreezeEffect(1),
    SleepEffect(1),
    StunEffect(1),
]:
    combat_manager.current_monster.effects = []
    combat_manager.current_monster.apply_effect(effect)

    combat_manager.take_turn()

# ----------------------------

print("\n===== Effect Activation: Being Attacked =====")

for effect in [ThornsEffect(1)]:
    combat_manager.current_monster.effects = []
    combat_manager.current_monster.apply_effect(effect)

    combat_manager.effect_manager.execute_effect(
        AttackEffect(1),
        source=monster_a,
        target=combat_manager.current_monster,
    )

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

print("\n===== Effect Limit =====")

combat_manager.current_monster.effects = []

for _ in range(10):
    combat_manager.current_monster.effects.append(RegenEffect(1))

combat_manager.logger.log_monster(combat_manager.current_monster)
