"""Scenario for testing damage logging."""

from copy import deepcopy

from colorama import init

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.base.stat import Stat
from src.base.team import Team
from src.combat.manager import CombatManager
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.fortify import FortifyEffect
from src.effects.fragile import FragileEffect
from src.effects.heal import HealEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.pierce import PierceEffect
from src.effects.sacred_block import SacredBlockEffect
from src.effects.strength import StrengthEffect
from src.effects.weak import WeakEffect
from src.systems.settings import Settings

init()

# ----------------------------

sides = []

for i in range(1, 4):
    sides.append(Side(effects=[AttackEffect(Stat(flat=i))]))
    sides.append(Side(effects=[DrainEffect(Stat(flat=i))]))
    sides.append(Side(effects=[PierceEffect(Stat(flat=i))]))
    sides.append(Side(effects=[HealEffect(Stat(flat=i))]))

dice_0 = Dice(sides=sides)

# ----------------------------

sides = []

for i in range(1, 4):
    sides.append(Side(effects=[AbsorbEffect(Stat(flat=i))]))
    sides.append(Side(effects=[BlockEffect(Stat(flat=i))]))
sides.append(Side(effects=[InvulnerableEffect()]))
sides.append(Side(effects=[SacredBlockEffect(Stat(flat=1))]))

dice_1 = Dice(sides=sides)

# ----------------------------

sides = []

for i in range(1, 4):
    sides.append(Side(effects=[FortifyEffect(Stat(flat=i), duration=3)]))
    sides.append(Side(effects=[FragileEffect(Stat(flat=i), duration=3)]))
    sides.append(Side(effects=[StrengthEffect(Stat(flat=i), duration=3)]))
    sides.append(Side(effects=[WeakEffect(Stat(flat=i), duration=3)]))

dice_2 = Dice(sides=sides)

# ----------------------------

monster = Monster(
    name="Monster",
    hp=15,
    max_hp=30,
    dice=[
        dice_0,
        dice_1,
        dice_2,
    ],
)

# ----------------------------

team_a = Team(
    name="A",
    members=[
        deepcopy(monster),
        deepcopy(monster),
    ],
)

team_b = Team(
    name="B",
    members=[
        deepcopy(monster),
        deepcopy(monster),
    ],
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
    order_strategy="SET",
)

# ----------------------------

combat_manager.run()
