"""Scenario for testing effect execution logging."""

from copy import deepcopy
from random import choice

from colorama import init

from src.base.color import Color, ColorData
from src.base.dice import Dice
from src.base.effect import EffectType
from src.base.keywords import Keyword
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.base.team import Team
from src.combat.manager import CombatManager
from src.combat.order_strategy import OrderStrategy
from src.compendium.effects import get_all_effects
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.bleed import BleedEffect
from src.effects.blind import BlindEffect
from src.effects.block import BlockEffect
from src.effects.burn import BurnEffect
from src.effects.cleanse import CleanseEffect
from src.effects.corrupt import CorruptEffect
from src.effects.doom import DoomEffect
from src.effects.drain import DrainEffect
from src.effects.execute import ExecuteEffect
from src.effects.focus import FocusEffect
from src.effects.fortify import FortifyEffect
from src.effects.fragile import FragileEffect
from src.effects.freeze import FreezeEffect
from src.effects.frostburn import FrostburnEffect
from src.effects.haste import HasteEffect
from src.effects.immunity import ImmunityEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.mana_regen import ManaRegenEffect
from src.effects.pierce import PierceEffect
from src.effects.poison import PoisonEffect
from src.effects.regen import RegenEffect
from src.effects.repel import RepelEffect
from src.effects.sacred_block import SacredBlockEffect
from src.effects.sleep import SleepEffect
from src.effects.slow import SlowEffect
from src.effects.strength import StrengthEffect
from src.effects.stun import StunEffect
from src.effects.taunt import TauntEffect
from src.effects.thorns import ThornsEffect
from src.effects.weak import WeakEffect
from src.systems.settings import Settings

init()

# ----------------------------

all_effects = get_all_effects()

for effect in all_effects:
    if effect.value is not None:
        if effect.value.flat is not None:
            effect.value.flat = 1

        if effect.value.percent is not None and effect.type in [
            EffectType.BUFF,
            EffectType.DEBUFF,
        ]:
            effect.value.percent = 0.5

    if effect.duration is not None:
        effect.duration = 2

# ----------------------------

monster_a = Monster(
    name="Monster",
    hp=150,
    max_hp=200,
)

team_a = Team(
    name="A",
    members=[monster_a],
)

monster_b = Monster(
    name="Monster",
    hp=150,
    max_hp=200,
)

team_b = Team(
    name="B",
    members=[monster_b],
)

# ----------------------------

combat_manager = CombatManager(
    settings=Settings(
        monster_end_turn="AUTO",
    ),
    teams=[
        team_a,
        team_b,
    ],
    order_strategy=OrderStrategy.SEQUENTIAL,
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
    monster_a.effects = [BlindEffect(Stat(flat=1))]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_b,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: Non-Persistable =====")

effect = FragileEffect(Stat(flat=99))

combat_manager.effect_manager.execute_effect(
    effect=effect,
    source=monster_a,
    target=monster_a,
)

effect = BlockEffect(Stat(flat=1))

combat_manager.effect_manager.execute_effect(
    effect=effect,
    source=monster_a,
    target=monster_a,
)

combat_manager.logger.log_monster(monster_a)

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: CLEANSE =====")

effects = []
for i in range(11):
    if i % 2 == 0:
        effect = BlindEffect(Stat(flat=1), duration=2)
    else:
        effect = BurnEffect(Stat(flat=1), duration=2)
    effects.append(effect)

for effect in [
    CleanseEffect(Stat(flat=0)),
    CleanseEffect(Stat(flat=1)),
    CleanseEffect(Stat(flat=5)),
    CleanseEffect(Stat(flat=6)),
    CleanseEffect(Stat(flat=10)),
]:
    monster_a.effects = effects[:i]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_a,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: CORRUPT =====")

effects = []
for i in range(11):
    if i % 2 == 0:
        effect = ManaRegenEffect(Stat(flat=1), duration=2)
    else:
        effect = RegenEffect(Stat(flat=1), duration=2)
    effects.append(effect)

for effect in [
    CorruptEffect(Stat(flat=0)),
    CorruptEffect(Stat(flat=1)),
    CorruptEffect(Stat(flat=5)),
    CorruptEffect(Stat(flat=6)),
    CorruptEffect(Stat(flat=10)),
]:
    monster_a.effects = effects[:i]

    combat_manager.effect_manager.execute_effect(
        effect=effect,
        source=monster_a,
        target=monster_a,
    )

monster_a.effects = []

# ----------------------------

print("\n===== Effect Execution: DOOM =====")

turns = 3

combat_manager.effect_manager.execute_effect(
    effect=DoomEffect(duration=turns),
    source=monster_b,
    target=monster_a,
)

for _ in range(turns + 2):
    combat_manager.end_turn()

combat_manager.current_monster.hp = 150

# ----------------------------

print("\n===== Effect Execution: EXECUTE =====")

monster_b.hp = 100

combat_manager.effect_manager.execute_effect(
    effect=ExecuteEffect(Stat(percent=0.5)),
    source=monster_a,
    target=monster_b,
)

monster_b.hp = 150

# ----------------------------

print("\n===== Effect Execution: IMMUNITY =====")

keywords = []
for i in range(11):
    if i % 2 == 0:
        keyword = Keyword.BURN
    else:
        keyword = Keyword.POISON
    keywords.append(keyword)

for i in [0, 1, 5, 6, 10]:
    immunity_effect = ImmunityEffect(target_keywords=keywords[:i])

    combat_manager.effect_manager.execute_effect(
        effect=immunity_effect,
        source=monster_b,
        target=monster_b,
    )

combat_manager.effect_manager.execute_effect(
    effect=BurnEffect(),
    source=monster_a,
    target=monster_b,
)

monster_b.effects = []

# ----------------------------

print("\n===== Effect Removal =====")

removal_sets = [
    (
        BlindEffect(),
        [FocusEffect()],
    ),
    (
        BurnEffect(),
        [FreezeEffect()],
    ),
    (
        FocusEffect(),
        [BlindEffect()],
    ),
    (
        FortifyEffect(),
        [FragileEffect()],
    ),
    (
        FragileEffect(),
        [FortifyEffect()],
    ),
    (
        FreezeEffect(),
        [BurnEffect()],
    ),
    (
        HasteEffect(),
        [SlowEffect()],
    ),
    (
        RepelEffect(),
        [TauntEffect()],
    ),
    (
        SleepEffect(),
        [
            AttackEffect(),
            DrainEffect(),
            PierceEffect(),
        ],
    ),
    (
        SlowEffect(),
        [HasteEffect()],
    ),
    (
        StrengthEffect(),
        [WeakEffect()],
    ),
    (
        TauntEffect(),
        [RepelEffect()],
    ),
    (
        WeakEffect(),
        [StrengthEffect()],
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

monster_b.effects = []

# ----------------------------

print("\n===== Effect Activation: Act Disabling =====")

combat_manager.current_monster = monster_a

for effect in [
    FreezeEffect(),
    SleepEffect(),
    StunEffect(),
]:
    monster_a.effects = [effect]

    combat_manager.take_turn()

monster_a.effects = []

# ----------------------------

print("\n===== Effect Activation: Being Attacked =====")

for effect in [
    AbsorbEffect(Stat(flat=1)),
    BlockEffect(Stat(flat=1)),
    InvulnerableEffect(target_keywords=[Keyword.ALL]),
    SacredBlockEffect(Stat(flat=1)),
    ThornsEffect(Stat(flat=1)),
]:
    monster_b.effects = [effect]

    combat_manager.effect_manager.execute_effect(
        AttackEffect(Stat(flat=2)),
        source=monster_a,
        target=monster_b,
    )

monster_b.effects = []

# ----------------------------

print("\n===== Effect Activation: Dice Roll =====")

combat_manager.current_monster.dice = [
    Dice(sides=[Side(effects=[AttackEffect(Stat(flat=1))])]),
]

for effect in [
    BleedEffect(Stat(flat=1)),
]:
    combat_manager.current_monster.effects = []
    combat_manager.current_monster.apply_effect(effect)

    combat_manager.start_turn()
    combat_manager.take_turn()

combat_manager.current_monster.dice = []
combat_manager.current_monster.effects = []

# ----------------------------

print("\n===== Effect Activation: Turn Start =====")

for effect in [
    BurnEffect(Stat(flat=1)),
    FrostburnEffect(Stat(flat=1)),
    ManaRegenEffect(Stat(flat=1)),
    PoisonEffect(Stat(flat=1)),
    RegenEffect(Stat(flat=1)),
]:
    combat_manager.current_monster.apply_effect(effect)

combat_manager.start_turn()

combat_manager.current_monster.effects = []

# ----------------------------

print("\n===== Effect Limit =====")

for i in [0, 1, 2, 5, 6, 10]:
    effects = []

    for _ in range(i):
        effect = deepcopy(choice(all_effects))
        effects.append(effect)

    combat_manager.current_monster.effects = effects
    combat_manager.logger.log_monster(combat_manager.current_monster)

combat_manager.current_monster.effects = []

# ----------------------------

print("\n===== Alternative colored monster =====")

color_data: ColorData = {
    "foreground_color": Color.PURPLE,
    "background_color": Color.YELLOW,
    "intensity": "BRIGHT",
}

effects = []

for _ in range(10):
    effect = deepcopy(choice(all_effects))
    effects.append(effect)

combat_manager.current_monster.effects = effects
combat_manager.logger.log_monster(combat_manager.current_monster, color_data=color_data)

combat_manager.current_monster.effects = []
