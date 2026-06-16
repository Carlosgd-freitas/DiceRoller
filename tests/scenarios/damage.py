from colorama import init

from src.base.dice import Dice
from src.base.monster import Monster
from src.base.side import Side
from src.combat.manager import CombatManager
from src.combat.team import Team
from src.effects.absorb import AbsorbEffect
from src.effects.attack import AttackEffect
from src.effects.block import BlockEffect
from src.effects.drain import DrainEffect
from src.effects.invulnerable import InvulnerableEffect
from src.effects.pierce import PierceEffect
from src.effects.sacred_block import SacredBlockEffect
from src.locales.languages import Language

init()

# ----------------------------

sides = []
for i in range(1, 7):
    sides.append(Side(effects=[AttackEffect(i)]))
    sides.append(Side(effects=[DrainEffect(i)]))
    sides.append(Side(effects=[PierceEffect(i)]))

monster_a = Monster(
    name="Monster",
    hp=15,
    max_hp=30,
    dice=[
        Dice(sides=sides),
    ],
)

team_a = Team(
    name="Red Team",
    members=[monster_a],
)

# ----------------------------

sides = []
for i in range(1, 4):
    sides.append(Side(effects=[AbsorbEffect(i)]))
    sides.append(Side(effects=[BlockEffect(i)]))

sides.append(Side(effects=[InvulnerableEffect()]))
sides.append(Side(effects=[SacredBlockEffect(1)]))

monster_b = Monster(
    name="Monster",
    hp=15,
    max_hp=30,
    dice=[
        Dice(sides=sides),
    ],
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

# ----------------------------

combat_manager.run()
